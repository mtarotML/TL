from sqlmodel import SQLModel, create_engine
from .models import User  # <- important !$

# URL de la base de données SQLite (fichier local)
DATABASE_URL = "sqlite:///./dating_app.db"

# Création du moteur SQLAlchemy/SQLModel
engine = create_engine(DATABASE_URL, echo=True)  # echo=True = logs SQL visibles

# Fonction utilitaire pour créer toutes les tables
def init_db():
    SQLModel.metadata.create_all(engine)
