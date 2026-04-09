#  TEKTAL — Backend

Backend du projet **Tektal **, une application permettant de créer, partager et suivre des chemins visuels (vidéo + étapes).

---

##  À propos

Tektal aide les utilisateurs (principalement des étudiants) à :

*  Trouver un lieu facilement grâce à des chemins visuels
*  Créer des parcours avec vidéo + étapes
*  Suivre un chemin étape par étape
*  Partager un chemin via lien
*  Accéder à des chemins officiels (écoles, entreprises)

  Objectif : construire un MVP rapide pour valider l’usage.

---

##  Stack technique

* Django
* Django REST Framework
* PostgreSQL
* Djoser (authentification)
* JWT (SimpleJWT)
* Cloudinary (stockage vidéo)

---

##  Structure du projet

```
tektal-backend/
│
├── accounts/
├── paths/
├── admin_panel/
├── manage.py
├── requirements.txt
└── .env.example
```

---

##  Installation complète

### 1. Cloner le projet

```bash
git clone https://github.com/ton-repo/tektal-backend.git
cd tektal-backend
```

---

### 2. Créer un environnement virtuel

```bash
python -m venv venv
```

#### Activer l’environnement

**Mac / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

---

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

##  Configuration des variables d’environnement

### 1. Créer le fichier `.env`

```bash
cp .env.example .env
```

 Sur Windows :

```bash
copy .env.example .env
```

---

### 2. Remplir `.env`

```env
# ======================
# DJANGO
# ======================
DJANGO_SECRET_KEY=#<metter votre secrt_key>
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# ======================
# DATABASE (LOCAL)
# ======================
# Utilisation SQLite en local
# (DATABASE_URL vide = fallback SQLite)
DATABASE_URL=

# ======================
# CLOUDINARY (LOCAL)
# ======================
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

BREVO_API_KEY=#< mettervotre api_key>
DEFAULT_FROM_EMAIL=TEKTAL #<metter votre mail d' inscription brevo>
DOMAIN=localhost:5173
PROTOCOL=http
SITE_NAME=TEKTAL

EMAIL_HOST_USER= # <metter votre mail de configuration ici>
EMAIL_HOST_PASSWORD=# <metter ici le mot de pass>

```

---

##  Base de données

Créer la base PostgreSQL :

```sql
CREATE DATABASE tektal_db;
```

---

##  Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

##  Créer un super utilisateur

```bash
python manage.py createsuperuser
```

---

##  Lancer le serveur

```bash
python manage.py runserver
```

 Accès :

```
http://127.0.0.1:8000/
```

---

##  Authentification

Système basé sur **Djoser + JWT avec activation email**

### Flow :

1. Inscription
2. Email d’activation
3. Activation du compte
4. Connexion
5. Accès avec token JWT

---

##  Fonctionnalité principale : Paths

* Création de chemins (vidéo + étapes)
* Navigation étape par étape
* Favoris
* Partage via lien
* GPS (début / fin)

---

##  Établissements

* Un établissement est un type d’utilisateur ou entité
* Peut publier des **chemins officiels**
* Le badge officiel est attribué par l’admin

 Le détail complet du flow est disponible dans la documentation (Wiki)

---

##  Endpoints principaux

### Auth

```
POST /api/auth/users/
POST /api/auth/users/activation/
POST /api/token/
POST /api/token/refresh/
GET  /api/auth/users/me/
```

---

### Paths

```
GET    /api/paths/
POST   /api/paths/create/
GET    /api/paths/{id}/
POST   /api/paths/{id}/favorite/
GET    /api/users/me/favorites/
GET    /api/paths/{id}/gps/
```

---

### Partage

```
POST /api/share/{token}/
GET  /share/{token}/
```

---

### Établissements

```
GET /api/establishments/
```

---

##  Tests

```bash
python manage.py test
```

---

##  Sécurité

* JWT Authentication
* Activation obligatoire des comptes
* Protection des endpoints
* Validation côté backend

---

##  Déploiement

Le backend peut être déployé facilement sur des plateformes cloud comme **Render** ou **Railway**.

---

###  Déploiement avec Render 

1. Créer un compte sur https://render.com  
2. Créer un nouveau **Web Service**
3. Connecter ton repository GitHub  
4. Configurer :

- **Build Command**
```bash
pip install -r requirements.txt

##  Contribution

1. Fork
2. Créer une branche

```bash
git checkout -b feature/ma-feature
```

3. Commit

```bash
git commit -m "feat: ma feature"
```

4. Push

```bash
git push origin feature/ma-feature
```

5. Pull Request

---

##  Documentation

 Disponible dans le **Wiki GitHub**

---

##  Auteur

Projet développé dans le cadre du MVP **Tektal Web**

---

##  Vision

Construire une solution simple et efficace pour guider les utilisateurs vers un lieu grâce à la vidéo et à l’expérience communautaire.
