import json
import asyncio
from fastapi import FastAPI, HTTPException, Header, Body, Depends
from pydantic import BaseModel
from typing import Optional
from secrets import token_hex
import base64
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation des dictionnaires
cle_store = {}
viewers = {}

# Chargement des données depuis "state.json" si le fichier existe
if os.path.exists("state.json"):
    try:
        with open("state.json", "r") as f:
            data = json.load(f)
            viewers = data.get("viewers", {})
            cle_store = data.get("cle_store", {})
            print("Données chargées depuis state.json")
    except Exception as e:
        print("Erreur lors du chargement de state.json :", e)
else:
    print("Aucun fichier state.json trouvé, initialisation des dictionnaires vides.")

class KeyPayload(BaseModel):
    owner_username: str
    image_id: str
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    valid: Optional[bool] = True

class ViewerPayload(BaseModel):
    viewer_username: str

class UpdateValidityPayload(BaseModel):
    valid: bool
    token: str  # Ajouté ici

@app.post("/set_key")
def set_key(payload: KeyPayload):
    generated_key = base64.b64encode(os.urandom(32)).decode()
    cle_store[payload.image_id] = {
        "owner_username": payload.owner_username,
        "key": generated_key,
        "valid": payload.valid
    }
    return {
        "message": "Clé enregistrée avec succès.",
        "key": generated_key,
    }

@app.post("/register_viewer")
def register_viewer(payload: ViewerPayload):
    if payload.viewer_username in viewers:
        return {"message": "Utilisateur déjà enregistré.", "token": viewers[payload.viewer_username]}
    token = token_hex(16)
    viewers[payload.viewer_username] = token
    return {"message": "Utilisateur enregistré avec succès.", "token": token}


@app.get("/trust_token/{username}")
def get_trust_token(username: str):
    if username not in viewers:
        raise HTTPException(status_code=404, detail="Utilisateur inconnu.")
    return {"token": viewers[username]}


@app.post("/get_key/{image_id}")
def get_key(image_id: str, payload: dict = Body(...)):
    viewer_username = payload.get("username")
    token = payload.get("token")
    if image_id not in cle_store:
        raise HTTPException(status_code=404, detail="Clé non trouvée.")

    key_data = cle_store[image_id]

    is_valid_viewer = (viewer_username in viewers and viewers[viewer_username] == token)
    if not is_valid_viewer:
        raise HTTPException(status_code=403, detail="Token ou identifiant utilisateur invalide.")

    if not key_data["valid"]:
        raise HTTPException(status_code=403, detail="Clé invalide ou expirée.")

    return {"key": key_data["key"]}

@app.delete("/delete_key/{username}/{image_id}")
def delete_key(username: str, image_id: str, token: Optional[str] = Header(None)):
    if (username, image_id) not in cle_store:
        raise HTTPException(status_code=404, detail="Clé non trouvée.")
    if token != cle_store[(username, image_id)]["token"]:
        raise HTTPException(status_code=403, detail="Token invalide.")
    del cle_store[(username, image_id)]
    return {"message": "Clé supprimée avec succès."}

@app.post("/update_validity/{owner_username}/{image_id}")
def update_validity(
    owner_username: str,
    image_id: str,
    payload: UpdateValidityPayload = Body(...)
):
    if image_id not in cle_store:
        raise HTTPException(status_code=404, detail="Clé non trouvée.")
    if cle_store[image_id]["owner_username"] != owner_username:
        raise HTTPException(status_code=403, detail="Nom d'utilisateur non autorisé.")
    if payload.token != viewers.get(owner_username):
        raise HTTPException(status_code=403, detail="Token invalide.")

    cle_store[image_id]["valid"] = payload.valid

    return {"message": f"Validité mise à jour : {payload.valid}"}


async def log_json_viewers_and_keys():
    while True:
        data = {
            "viewers": viewers,
            "cle_store": cle_store
        }
        with open("state.json", "w") as f:
            json.dump(data, f, indent=4)
        await asyncio.sleep(1)


import requests
import random

async def ping_other_backend():
    while True:
        try:
            def make_request():
                response = requests.get("https://secugram.onrender.com/auth/login")
                print(f"Requête vers /all OK : {response.status_code}")
            await asyncio.to_thread(make_request)
        except Exception as e:
            print(f"Erreur lors de l'appel à /all : {e}")
        PING_INTERVAL_SECONDS = random.randint(300, 600)
        await asyncio.sleep(PING_INTERVAL_SECONDS)


@app.on_event("startup")
async def schedule_background_tasks():
    asyncio.create_task(log_json_viewers_and_keys())
    asyncio.create_task(ping_other_backend())

