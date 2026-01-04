from sqlmodel import SQLModel, create_engine
from .models import User  # <- important !$
from .core.config import settings

DATABASE_URL = settings.DATABASE_URL

# Création du moteur SQLAlchemy/SQLModel
engine = create_engine(DATABASE_URL, echo=True)  # echo=True = logs SQL visibles

# Fonction utilitaire pour créer toutes les tables
def init_db():
    SQLModel.metadata.create_all(engine)
