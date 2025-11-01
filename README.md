# TrueLink

Petit projet entre amis pour tester **FastAPI** et **SQLModel**.

---

## 🔧 Fonctionnement global

Le projet est découpé en deux parties :

- **Backend** : FastAPI + SQLModel (API, authentification, base SQLite)  
- **Frontend** : HTML / JS statique servi directement par FastAPI  

L’API permet :  
- d’enregistrer un utilisateur,  
- de se connecter,  
- et de générer un **token JWT** pour l’authentification.  

---

## 🧰 Script utilitaire : `merge_py_files.py`

Ce script fusionne **tous les fichiers texte du projet** (`.py`, `.html`, `.js`, `.md`, etc.)  
dans un seul fichier nommé **`all_text_files_merged.txt`**.

💡 *Pratique pour relire le projet complet ou le partager facilement.*

### Utilisation
```bash
python merge_py_files.py
```

---

## 👑 Page admin cachée

Accessible via :  
```
/admin
```

Mot de passe par défaut : `admin`  
⚠️ *À déplacer dans un `.env` pour un usage en production.*

Cette page affiche une **table HTML des utilisateurs inscrits**,  
directement tirée de la base de données SQLite.

---

## ⚙️ Lancer le projet

```bash
cd TL_backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend accessible sur :  
```
http://127.0.0.1:8000
```

---

> Projet fun, léger, et prêt à être bricolé 🔧
