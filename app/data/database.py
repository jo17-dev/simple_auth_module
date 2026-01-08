from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from config.env import settings

# Chemin du fichier database.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Création du moteur SQLAlchemy
engine = create_engine(settings.DATABASE_URL, echo=True)

# Configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour tous les modèles
Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()