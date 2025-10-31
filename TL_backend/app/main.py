from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from .database import init_db
from .routes import users, auth
import os
from fastapi import Request, HTTPException, Form
from sqlmodel import Session, select
from fastapi.responses import HTMLResponse
from .models import User
from .database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("✅ Database initialized.")
    yield
    print("🛑 Shutting down app...")

app = FastAPI(lifespan=lifespan)

# Inclusion des routes
app.include_router(users.router)
app.include_router(auth.router)

# Servir les fichiers statiques
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "TL_frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def read_index():
    index_file = os.path.join(frontend_path, "index.html")
    return FileResponse(index_file)









ADMIN_PASSWORD = "admin"  # ⚠️ À mettre dans .env plus tard

@app.get("/admin", response_class=HTMLResponse)
def admin_login_page():
    return """
    <html>
        <body style='font-family: Arial; text-align: center; margin-top: 100px;'>
            <h2>🔒 Accès administrateur</h2>
            <form action="/admin" method="post">
                <input type="password" name="password" placeholder="Mot de passe" required />
                <button type="submit">Entrer</button>
            </form>
        </body>
    </html>
    """

@app.post("/admin", response_class=HTMLResponse)
def admin_dashboard(password: str = Form(...)):
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    with Session(engine) as session:
        users = session.exec(select(User)).all()

    rows = "".join(
        f"<tr><td>{u.id}</td><td>{u.username}</td><td>{u.email}</td><td>{u.hashed_password}</td></tr>"
        for u in users
    )

    return f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial; text-align: center; margin-top: 40px; }}
                table {{
                    margin: auto;
                    border-collapse: collapse;
                    width: 80%;
                }}
                th, td {{
                    border: 1px solid #ccc;
                    padding: 8px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <h2>👑 Tableau de bord administrateur</h2>
            <table>
                <tr><th>ID</th><th>Nom</th><th>Email</th><th>Mot de passe haché</th></tr>
                {rows or "<tr><td colspan='4'>Aucun utilisateur trouvé</td></tr>"}
            </table>
            <br>
            <a href="/">Retour à l'accueil</a>
        </body>
    </html>
    """

