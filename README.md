# 🚀 API et Interface de Gestion des Héros de Science-Fiction

Un projet complet avec API FastAPI, scripts de traitement et interface Streamlit pour gérer une base de données de personnages de science-fiction.

## ✨ Fonctionnalités

### API FastAPI
- **Gestion CRUD** des héros (Create, Read, Update, Delete)
- **Système d'authentification** par token
- **Webhooks** pour recevoir de nouveaux personnages
- **Traitement de données** avec calcul automatique de niveau
- **Système de notifications** configurable

### Interface Streamlit
- 📜 Explorateur visuel des héros
- 🤖 Envoi de personnages via webhook
- ⚙️ Traitement par lots des données
- 🔔 Gestion des notifications

## 🛠 Installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/votre-utilisateur/heroes-sf-api.git
cd heroes-sf-api
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer Stripe** (optionnel)
Créez un fichier `.env` avec votre clé Stripe:
```
STRIPE_SECRET_KEY=votre_clé_secrète
```

## 🚀 Lancement

1. **Démarrer l'API FastAPI**
```bash
uvicorn main:app --reload
```

2. **Lancer l'interface Streamlit** (dans un autre terminal)
```bash
streamlit run app_streamlit.py
```

3. **Accéder aux interfaces**
- API: http://localhost:8000
- Documentation Swagger: http://localhost:8000/docs
- Interface Streamlit: http://localhost:8501
- Frontend simple: http://localhost:8000/frontend

## 📚 Endpoints API

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/heros` | GET | Liste tous les héros |
| `/heros` | POST | Ajoute un nouveau héros |
| `/heros/{nom}` | PUT | Met à jour un héros |
| `/heros/{nom}` | DELETE | Supprime un héros |
| `/webhook/personnage` | POST | Webhook pour nouveaux personnages |
| `/traitement` | POST | Enrichit les données d'un personnage |
| `/subscribe/{etat}` | POST | Gère les abonnements |


## 🔧 Technologies Utilisées

- Python 3.9+
- FastAPI
- Streamlit
- Pydantic
- Requests
- Stripe (optionnel)

