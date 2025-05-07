# 🧙 Frontend React — Gestion de Personnages

faire deja 
cd frontend

Ce projet est l’interface frontend d’une application de gestion de personnages fictifs, connectée à une API FastAPI. Il permet d'ajouter, modifier, supprimer et filtrer les personnages, et d'interagir avec une API backend sécurisée.

## ⚙️ Fonctionnalités

- Affichage d’une liste de personnages
- Ajout, modification et suppression de personnages via des modales
- Filtrage par nom et univers
- Chargement d’exemples de personnages
- Appels à une API protégée par un token

## 🧱 Stack utilisée

- React + TypeScript
- TailwindCSS (ou autre framework selon la config)
- Hooks personnalisés
- Appels API via `fetch` (cf. fichier `api.ts`)

## 🚀 Lancer le projet

### 1. Installer les dépendances

```bash
npm install
```

### 2. Lancer le serveur de développement

```bash
npm run dev
```

> Par défaut, l'application est disponible sur `http://localhost:5173`

## 🔑 Authentification API

Les appels API utilisent un token d’authentification simple, transmis dans les en-têtes HTTP :
```
token: mytoken123
```

Assure-toi que l’API backend tourne sur `http://localhost:8000` (ou adapte l’URL dans `api.ts` si nécessaire).

## 📁 Structure principale

```
.
├── src/
│   ├── components/               # Composants UI (Header, List, Modales)
│   ├── hooks/                    # Hooks personnalisés (ex: useCharacterOperations)
│   ├── types/                    # Types TypeScript (ex: Character)
│   ├── api.ts                    # Fonctions pour appels API
│   └── pages/Index.tsx          # Page principale
```

## 💬 Interaction avec le Backend

- `GET /personnages` → liste les personnages
- `POST /personnages` → ajoute un personnage
- `PUT /personnages/{nom}` → modifie un personnage
- `DELETE /personnages/{nom}` → supprime un personnage
- `GET /personnages/exemple` → charge des exemples

## 📬 Contact

Projet React utilisé avec un backend FastAPI — idéal pour l'apprentissage complet d'une app fullstack.
