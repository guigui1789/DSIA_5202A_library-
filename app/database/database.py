from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion à la base de données PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db/library_db"

# Création de l'engine de base de données
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Session pour interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles déclaratifs
Base = declarative_base()
