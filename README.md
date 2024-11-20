# DSIA_5202A_pers_library

http://localhost:8000/docs

bearer
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTczMjA4MTY0MX0.OLB4Da4MyruIeLYM3u6zYak9wNsDLVkQ3-cwDvMDh0I



# Personal Library API

## Description
Cette API permet de gérer une bibliothèque personnelle avec des fonctionnalités telles que :
- Gestion des utilisateurs avec authentification via JWT.
- Gestion des livres (CRUD : Create, Read, Update, Delete).
- Endpoints sécurisés nécessitant une authentification.
- Déploiement simple avec Docker Compose.

## Fonctionnalités
- **Authentification :**
  - Récupération d'un token JWT à l'aide d'un nom d'utilisateur et d'un mot de passe.
  - Accès à des endpoints protégés avec un token JWT valide.
- **Gestion des livres :**
  - Ajouter un livre.
  - Consulter la liste des livres.
  - Consulter les détails d’un livre spécifique par son ID.
  - Supprimer un livre par son ID.
- **Endpoints sécurisés :**
  - Certains endpoints nécessitent des permissions spécifiques ou un rôle particulier.
    
## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- [Docker](https://www.docker.com/get-started) et [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.9 (si vous souhaitez exécuter le projet en local sans Docker)

## Installation

1. Clonez le dépôt :
   ```bash
   git clone <URL_DU_DEPOT>
   cd DSIA_5202A_pers_library

2. Démarrez les services avec Docker Compose :
   ```bash
   docker-compose up --build

   Cela construira et démarrera :
      - Le service API écrit en Python avec FastAPI.
      - Une base de données PostgreSQL.

3. Une fois démarré, accédez à la documentation interactive de l'API :
    Rendez-vous sur http://localhost:8000/docs.

## Structure du Projet

DSIA_5202A_pers_library/
├── app/
│   ├── auth.py                  # Gestion de l'authentification JWT
│   ├── database/
│   │   ├── database.py          # Configuration de la base de données avec SQLAlchemy
│   ├── models/
│   │   ├── user.py              # Modèle utilisateur
│   │   ├── book.py              # Modèle livre
│   ├── schemas/
│   │   ├── user_schema.py       # Schéma utilisateur
│   │   ├── book_schema.py       # Schéma livre
│   ├── main.py                  # Point d'entrée de l'application FastAPI
│   ├── test_main.py             # Tests unitaires pour l'API
├── data/
│   ├── db/                      # Fichiers de données PostgreSQL
├── Dockerfile                   # Dockerfile pour construire l'image de l'API
├── docker-compose.yml           # Configuration Docker Compose
├── requirements.txt             # Dépendances Python


Endpoints
Publics
POST /token : Récupérer un token JWT en fournissant un nom d'utilisateur et un mot de passe.
GET / : Endpoint de test de connexion.
Protégés (JWT requis)
GET /books/ : Récupérer la liste des livres.
POST /books/ : Ajouter un livre.
GET /books/{book_id} : Récupérer un livre par ID.
DELETE /books/{book_id} : Supprimer un livre par ID.

Technologies Utilisées
Framework API : FastAPI
Base de données : PostgreSQL
ORM : SQLAlchemy
Authentification : JWT
Gestion des conteneurs : Docker et Docker Compose

Auteur
Votre Nom - Étudiant E5
Contact : votre-email@example.com

