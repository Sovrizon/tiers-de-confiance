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



## 🚀 Installation

### 1. Cloner le dépôt :

```bash
git clone https://github.com/Sovrizon/tiers-de-confiance.git
cd tiers-de-confiance
```

### 2. Installer les dépendances :

```bash
pip install -r requirements.txt
```


### 3. Configuration de MongoDB 


#### Installation de MongoDB et mongosh
- Pour installer MongoDB : [Guide d'installation](https://www.mongodb.com/docs/manual/installation/)
- Pour installer mongosh : [Guide d'installation](https://www.mongodb.com/docs/mongodb-shell/install/)


#### Simplification avec Cloud MongoDB

Vous pouvez également utiliser un service de base de données cloud comme [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) pour éviter d'installer MongoDB localement.


#### Installation de MongoDB localement

Si vous souhaitez utiliser MongoDB localement, vous devez créer un utilisateur avec les droits d'accès à la base de données. Voici comment procéder : [tutoriel](https://www.mongodb.com/resources/products/fundamentals/create-database).






#### Configuration du fichier .env pour le backend

Créez un fichier `.env` à la racine du projet avec la variable suivante :

```
MONGO_URI="mongodb://<username>:<password>@localhost:27017" # local
```

ou

```
MONGO_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/test" # cloud
```



### 4. Lancer l'application :

```bash
uvicorn main:app --reload --port 8300
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
