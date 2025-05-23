import json
import asyncio
from fastapi import FastAPI, HTTPException, Header, Body, Depends
from pydantic import BaseModel
from typing import Optional
from secrets import token_hex
import base64
import os
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient, errors
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)


try:
    print("[INFO] Connexion à MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client["tiers-de-confiance"]
    print("[OK] Connexion établie.")
except errors.ConnectionFailure as e:
    print(f"[ERREUR] Échec de connexion : {e}")
    exit(1)



try:
    collections = db.list_collection_names()
    print(f"[INFO] Collections existantes : {collections}")

    if "keys" not in collections:
        print("[INFO] Création de la collection 'keys'...")
        db.create_collection("keys")
        print("[OK] Collection 'keys' créée.")

    if "tokens" not in collections:
        print("[INFO] Création de la collection 'tokens'...")
        db.create_collection("tokens")
        print("[OK] Collection 'tokens' créée.")

    keys_col = db["keys"]
    tokens_col = db["tokens"]
    print("[OK] Accès aux collections réussi.")
    
except errors.PyMongoError as e:
    print(f"[ERREUR] Problème lors de l'accès ou la création des collections : {e}")
    exit(1)




app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    token: str


@app.post("/set_key")
def set_key(payload: KeyPayload):
    generated_key = base64.b64encode(os.urandom(32)).decode()

    # Check if a key for this image_id already exists
    existing_key = keys_col.find_one({"image_id": payload.image_id})

    if existing_key:
        # Update existing key
        keys_col.update_one(
            {"image_id": payload.image_id},
            {"$set": {
                "owner_username": payload.owner_username,
                "key": generated_key,
                "valid": payload.valid,
                "valid_from": payload.valid_from,
                "valid_to": payload.valid_to
            }}
        )
    else:
        # Insert new key
        keys_col.insert_one({
            "image_id": payload.image_id,
            "owner_username": payload.owner_username,
            "key": generated_key,
            "valid": payload.valid,
            "valid_from": payload.valid_from,
            "valid_to": payload.valid_to
        })

    return {
        "message": "Clé enregistrée avec succès.",
        "key": generated_key,
    }


@app.post("/register_viewer")
def register_viewer(payload: ViewerPayload):
    existing_viewer = tokens_col.find_one({"username": payload.viewer_username})

    if existing_viewer:
        return {"message": "Utilisateur déjà enregistré.", "token": existing_viewer["token"]}

    token = token_hex(16)
    tokens_col.insert_one({
        "username": payload.viewer_username,
        "token": token
    })

    return {"message": "Utilisateur enregistré avec succès.", "token": token}


@app.get("/trust_token/{username}")
def get_trust_token(username: str):
    viewer = tokens_col.find_one({"username": username})
    if not viewer:
        raise HTTPException(status_code=404, detail="Utilisateur inconnu.")

    return {"token": viewer["token"]}


@app.post("/get_key/{image_id}")
def get_key(image_id: str, payload: dict = Body(...)):
    viewer_username = payload.get("username")
    token = payload.get("token")

    # Check if key exists
    key_data = keys_col.find_one({"image_id": image_id})
    if not key_data:
        raise HTTPException(status_code=404, detail="Clé non trouvée.")

    # Verify viewer token
    viewer = tokens_col.find_one({"username": viewer_username})
    is_valid_viewer = viewer and viewer["token"] == token

    if not is_valid_viewer:
        raise HTTPException(status_code=403, detail="Token ou identifiant utilisateur invalide.")

    if not key_data["valid"]:
        raise HTTPException(status_code=403, detail="Clé invalide ou expirée.")

    return {"key": key_data["key"]}


@app.delete("/delete_key/{username}/{image_id}")
def delete_key(username: str, image_id: str, token: Optional[str] = Header(None)):
    key_data = keys_col.find_one({"image_id": image_id, "owner_username": username})

    if not key_data:
        raise HTTPException(status_code=404, detail="Clé non trouvée.")

    viewer = tokens_col.find_one({"username": username})
    if not viewer or viewer["token"] != token:
        raise HTTPException(status_code=403, detail="Token invalide.")

    keys_col.delete_one({"image_id": image_id, "owner_username": username})
    return {"message": "Clé supprimée avec succès."}


@app.post("/update_validity/{owner_username}/{image_id}")
def update_validity(
        owner_username: str,
        image_id: str,
        payload: UpdateValidityPayload = Body(...)
):
    key_data = keys_col.find_one({"image_id": image_id})

    if not key_data:
        raise HTTPException(status_code=404, detail="Clé non trouvée.")

    if key_data["owner_username"] != owner_username:
        raise HTTPException(status_code=403, detail="Nom d'utilisateur non autorisé.")

    viewer = tokens_col.find_one({"username": owner_username})
    if not viewer or viewer["token"] != payload.token:
        raise HTTPException(status_code=403, detail="Token invalide.")

    keys_col.update_one(
        {"image_id": image_id},
        {"$set": {"valid": payload.valid}}
    )

    return {"message": f"Validité mise à jour : {payload.valid}"}
