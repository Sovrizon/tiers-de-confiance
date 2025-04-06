# 🔐 Sovrizon - Tiers de Confiance

Ce dépôt contient le code source du **serveur tiers de confiance** pour le projet Sovrizon, un système décentralisé de gestion des données personnelles.

---

## 🎯 Objectif

Le tiers de confiance est un composant essentiel du système Sovrizon. Il est responsable de :
- La **génération de clés** de chiffrement pour les images
- Le **stockage sécurisé** des clés dans une base de données
- La **délivrance contrôlée** des clés aux utilisateurs autorisés

---

## 🧱 Technologies

- **Backend**: Python, FastAPI
- **Base de données**: MongoDB
- **Sécurité**: Génération de tokens, clés de chiffrement base64

---

## 🌐 Dépendances externes

- **Frontend Secugram** : [https://secugram-82493.web.app/](https://secugram-82493.web.app/)
- **Backend Secugram** : [https://secugram.onrender.com/docs](https://secugram.onrender.com/docs)
- **Documentation API** : [https://tiers-de-confiance.onrender.com/docs](https://tiers-de-confiance.onrender.com/docs)

---

## 🚀 Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/Sovrizon/tiers-de-confiance.git
cd tiers-de-confiance
```

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement :

Créez un fichier `.env` à la racine du projet avec les variables suivantes :
```
MONGO_USERNAME=votre_username_mongodb
MONGO_PASSWORD=votre_password_mongodb
```

4. Lancer l'application :

```bash
uvicorn main:app --reload
```

---

## 📦 Fonctionnalités

- 🔑 **Génération et stockage** de clés de chiffrement
- 👤 **Enregistrement des utilisateurs** (viewers)
- 🔐 **Vérification des tokens** d'authentification
- 🛡️ **Contrôle d'accès** aux clés basé sur les droits utilisateurs
- 🚦 **Gestion de la validité** des clés (activation/désactivation)
- 🔄 **Communication automatique** avec le backend principal
- 💾 **Persistance MongoDB** pour les clés et tokens de confiance

---

## 🔌 API Endpoints

### Gestion des clés

- **POST /set_key** : Génère et stocke une nouvelle clé pour une image
- **GET /get_key/{image_id}** : Récupère la clé pour une image spécifique
- **DELETE /delete_key/{username}/{image_id}** : Supprime une clé
- **POST /update_validity/{owner_username}/{image_id}** : Met à jour la validité d'une clé

### Gestion des utilisateurs

- **POST /register_viewer** : Enregistre un nouvel utilisateur
- **GET /trust_token/{username}** : Récupère le token de confiance d'un utilisateur

---

## 🧩 Intégration système

Ce serveur est conçu pour fonctionner en conjonction avec :
- L'application web [secugram](https://github.com/Sovrizon/secugram) qui chiffre les images
- L'[extension Chrome](https://github.com/Sovrizon/extension) qui déchiffre les images

---

## 👥 Auteurs et Contribution

Ce projet a été développé par :
- **Rémy GASMI** 
- **Simon VINCENT** 
- **Loqmen ANANI** 


---

## 📄 Licence

© 2025 Sovrizon – Tous droits réservés.
