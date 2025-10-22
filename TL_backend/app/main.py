from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import init_db
from .routes import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage de l'application
    init_db()
    print("✅ Database initialized.")
    yield
    # Arrêt de l'application
    print("🛑 Shutting down app...")

app = FastAPI(lifespan=lifespan)

# Inclusion du routeur utilisateur
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Dating API running with lifespan!"}
