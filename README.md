# Personal Library API

## Description

Le projet consiste en la création d'une API de bibliothèque personnelle. Cette API a pour objectif de permettre aux utilisateurs de gérer leurs livres via une interface simple et sécurisée. Les fonctionnalités principales incluent la possibilité de créer un utilisateur, de s'authentifier via un système d'authentification basé sur des tokens JWT, et d'effectuer des opérations CRUD (Create, Read, Update, Delete) sur une liste de livres.
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
   ``` 

   Cela construira et démarrera :
      - Le service API écrit en Python avec FastAPI.
      - Une base de données PostgreSQL.

3. Une fois démarré, accédez à la documentation interactive de l'API :
    Rendez-vous sur http://localhost:8000/docs.

## Endpoints
- **Publics**
- POST /token : Récupérer un token JWT en fournissant un nom d'utilisateur et un mot de passe.
- GET / : Endpoint de test de connexion.
- **Protégés (JWT requis)**
- GET /books/ : Récupérer la liste des livres.
- POST /books/ : Ajouter un livre.
- GET /books/{book_id} : Récupérer un livre par ID.
- DELETE /books/{book_id} : Supprimer un livre par ID.

## Difficultés rencontrées
La réalisation du projet a présenté plusieurs défis, notamment :

**Structure du projet et gestion des imports :**

- La structuration des fichiers et des dossiers (modèles, schémas, configuration de la base de données, etc.) a nécessité une attention particulière pour garantir une organisation claire et éviter des problèmes d'importation circulaire ou manquante.
- Certaines erreurs, comme ImportError, ont été rencontrées et corrigées en revoyant les chemins relatifs et en adoptant une structure modulaire.

**Connexion à la base de données avec Docker :**

- L'intégration de PostgreSQL avec Docker a posé quelques problèmes de connexion au début, notamment lorsque l'API démarrait avant que la base de données ne soit totalement prête.
- La solution a consisté à ajouter une logique de "retry" dans le code pour attendre que PostgreSQL soit disponible.

**Authentification et sécurité des endpoints :**

- L'implémentation de l'authentification avec JWT a nécessité une compréhension approfondie de la sécurisation des endpoints, notamment pour protéger les routes sensibles et gérer les erreurs liées aux tokens invalides ou expirés.

**Erreurs HTTP et gestion des exceptions :**

L'ajout d'une gestion complète des erreurs HTTP pour éviter les réponses génériques (500) a demandé un effort pour implémenter des réponses personnalisées et pertinentes (404, 401, 403, etc.).

## Conclusion
Malgré ces défis, le projet a abouti à une **API fonctionnelle** qui répond aux critères principaux :

- Gestion des utilisateurs avec JWT.
- CRUD complet pour les livres.
- Déploiement simple avec Docker.
- Documentation interactive accessible via Swagger.

## Technologies Utilisées
- Framework API : FastAPI
- Base de données : PostgreSQL
- ORM : SQLAlchemy
- Authentification : JWT
- Gestion des conteneurs : Docker et Docker Compose

## Auteur
Quentin Guigui & Quentin Lebouc - E5 DSIA                    Contact : quentin.guigui@edu.esiee.fr
          quentin.lebouc@edu.esiee.fr
