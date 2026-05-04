# Haiti Reh-Care

Site web complet pour Haiti Reh-Care — Centre de réhabilitation et d'appareillage orthopédique à Delmas 75, Haïti.

## Structure du projet

```
haiti-rehcare/
├── frontend/          # Site web (HTML/CSS/JS)
│   ├── index.html
│   ├── pages/
│   └── assets/
│       ├── css/
│       ├── js/
│       └── img/
└── backend/           # API FastAPI (Python)
    ├── main.py
    ├── routers/
    ├── models/
    └── utils/
```

## Technologies

### Frontend
- HTML5 sémantique
- CSS3 avec variables CSS
- JavaScript vanilla (ES6+)
- Lucide Icons (CDN)
- GSAP pour animations
- Chart.js pour graphiques admin

### Backend
- FastAPI (Python)
- SQLAlchemy (ORM)
- SQLite (base de données)
- JWT Authentication
- CORS enabled

## Fonctionnalités

### Site public
- [x] Page d'accueil avec hero section
- [x] Présentation des services (6 spécialités)
- [x] Présentation de l'équipe
- [x] Blog médical
- [x] Galerie photos
- [x] Page de dons
- [x] Formulaire de contact
- [x] Prise de rendez-vous en ligne

### Espace patient
- [x] Inscription / Connexion
- [x] Tableau de bord personnel
- [x] Historique des rendez-vous
- [x] Suivi des traitements
- [x] Documents médicaux

### Administration
- [x] Tableau de bord avec statistiques
- [x] Gestion des rendez-vous (calendrier)
- [x] Gestion des patients (dossiers)
- [x] Gestion du blog (CRUD)
- [x] Gestion de la galerie
- [x] Gestion de l'équipe
- [x] Paramètres du site

## Déploiement

### Backend (Render.com)

1. Créer un compte sur [Render.com](https://render.com)
2. Connecter votre repository GitHub
3. Créer un nouveau Web Service
4. Configuration:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Définir les variables d'environnement dans le fichier `.env` ou dans Render

### Frontend (Netlify ou Render Static)

1. Option 1: **Netlify**
   - Déployer le dossier `frontend/` directement
   - Configurer les redirections SPA si nécessaire

2. Option 2: **Render Static Site**
   - Créer un Static Site sur Render
   - Pointer vers le dossier `frontend/`

## Installation locale

### Prérequis
- Python 3.9+
- Node.js (optionnel pour certains outils)

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

# Créer le fichier .env
cp .env.example .env

# Lancer le serveur
uvicorn main:app --reload
```

Le backend sera accessible à `http://localhost:8000`

Documentation API: `http://localhost:8000/docs`

### Frontend

Le frontend est constitué de fichiers statiques HTML. Vous pouvez:

1. Ouvrir les fichiers HTML directement dans le navigateur
2. Utiliser un serveur local:
   ```bash
   cd frontend
   python -m http.server 3000
   ```

Le frontend sera accessible à `http://localhost:3000`

## Identifiants par défaut

### Admin
- Email: `admin@haiti-rehcare.org`
- Password: `ChangeThisPassword123!` (à modifier dans les variables d'environnement)

## Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `DATABASE_URL` | URL de la base de données | `sqlite+aiosqlite:///./haiti_rehcare.db` |
| `SECRET_KEY` | Clé secrète JWT | Générer une clé sécurisée |
| `ADMIN_EMAIL` | Email administrateur | `admin@haiti-rehcare.org` |
| `ADMIN_PASSWORD` | Mot de passe admin | À changer impérativement |
| `UPLOAD_DIR` | Dossier uploads | `uploads` |

## API Endpoints

### Authentification
- `POST /auth/login` - Connexion
- `POST /auth/register` - Inscription patient

### Rendez-vous
- `GET /appointments/slots?appointment_date=YYYY-MM-DD` - Créneaux disponibles
- `POST /appointments/` - Créer un rendez-vous
- `GET /appointments/` - Liste des rendez-vous (admin)
- `PATCH /appointments/{id}/status` - Modifier statut (admin)

### Patients
- `POST /patients/` - Créer un patient
- `GET /patients/` - Liste des patients (admin)
- `GET /patients/{id}` - Détails d'un patient (admin)
- `PATCH /patients/{id}` - Modifier un patient (admin)

### Blog
- `GET /blog/` - Liste des articles
- `GET /blog/{slug}` - Détails d'un article
- `POST /blog/` - Créer un article (admin)
- `PATCH /blog/{id}` - Modifier un article (admin)
- `DELETE /blog/{id}` - Supprimer un article (admin)

### Galerie
- `GET /gallery/` - Liste des images
- `POST /gallery/upload` - Upload image (admin)
- `PATCH /gallery/{id}` - Modifier une image (admin)
- `DELETE /gallery/{id}` - Supprimer une image (admin)

## Sécurité

- Authentification JWT avec expiration (24h par défaut)
- Hashage des mots de passe avec bcrypt
- Validation des entrées utilisateur
- CORS configuré pour les origines autorisées
- Limite de taille des fichiers uploadés (5MB)

## Maintenance

### Sauvegarde de la base de données
```bash
# SQLite - simplement copier le fichier
sqlite3 haiti_rehcare.db ".backup haiti_rehcare_backup.db"
```

### Mise à jour
```bash
# Mettre à jour les dépendances
pip install -U -r requirements.txt
```

## Support

Pour toute question ou problème:
- Email: haitirehabilitationcare@gmail.com
- Téléphone: +509 3644-1617

## Licence

© 2025 Haiti Reh-Care. Tous droits réservés.

---

**Confortabilité - Esthéticité - Fonctionalité**
