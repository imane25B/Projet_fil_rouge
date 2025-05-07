Voici une version reformulée et réorganisée de ton `README.md` dans un format clair, professionnel et agréable à lire :

---

# 🚀 FastAPI Sci-Fi Characters API + Stripe Webhook

Bienvenue dans ce projet FastAPI 👽 !
Cette API vous permet de **gérer des personnages emblématiques** issus de l’univers de la science-fiction (Star Wars, Blade Runner, Matrix...) tout en intégrant un **webhook Stripe sécurisé** pour écouter des événements de paiement.

---

## ⚙️ Technologies utilisées

* **Python 3.x**
* **FastAPI** (framework web ultra-rapide)
* **Pydantic** (validation de données)
* **Stripe SDK** (gestion des événements de paiement)
* **JSON** (fichier local comme base de données)
* **Uvicorn** (serveur ASGI rapide)

---

## 🧰 Fonctionnalités principales

✅ Authentification par token
🗃️ Sauvegarde locale dans un fichier JSON
📡 Webhook Stripe : écoute les événements `checkout.session.completed`
🌐 CORS activé (connexion possible depuis un frontend)

---

## 🚀 Lancement de l'application

1. **Se placer dans le bon dossier**

```bash
cd backendAPI
```

2. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

> Ou si tu n’as pas de fichier `requirements.txt` :

```bash
pip install fastapi uvicorn stripe
```

3. **Démarrer le serveur**

```bash
uvicorn main:app --reload
```

---

## 🔐 Authentification

Certaines routes sont sécurisées.
Pour y accéder, ajoute ce header HTTP :

```
token: mytoken123
```

---

## 👽 Endpoints — API Personnages SF

| Méthode | URL                    | Description                                               |
| ------- | ---------------------- | --------------------------------------------------------- |
| GET     | `/personnages`         | Récupère la liste complète des personnages (token requis) |
| POST    | `/personnages`         | Ajoute un nouveau personnage (token requis)               |
| PUT     | `/personnages/{nom}`   | Modifie un personnage existant (token requis)             |
| DELETE  | `/personnages/{nom}`   | Supprime un personnage (token requis)                     |
| GET     | `/personnages/exemple` | Renvoie 3 exemples de personnages de science-fiction      |

---

## 💳 Webhook Stripe

### 📬 Endpoint

```http
POST /webhook/stripe
```

### 🔧 Configuration sur Stripe

1. Va sur [https://dashboard.stripe.com](https://dashboard.stripe.com)

2. Menu **Développeurs > Webhooks**

3. Crée un nouvel endpoint :

   * **URL** : `http://localhost:8000/webhook/stripe`
   * **Événement écouté** : `checkout.session.completed`

4. Copie la **clé de signature secrète** et remplace-la dans ton code :

```python
WEBHOOK_SECRET = "whsec_votre_cle_secrete"
```

---

### 🧪 Tester localement avec Stripe CLI

```bash
stripe listen --forward-to localhost:8000/webhook/stripe
```

Déclenche ensuite un événement test :

```bash
stripe trigger checkout.session.completed
```

---

## 📁 Structure du projet

```bash
.
├── main.py               # Application FastAPI principale
├── personnages.json      # Données locales (fichier JSON)
└── README.md             # Documentation du projet
```

---

## ✨ Exemples de personnages intégrés

* **Luke Skywalker** – *Star Wars*
* **Ellen Ripley** – *Alien*
* **Rick Deckard** – *Blade Runner*

---

## 🧑‍💻 À propos

Projet pédagogique conçu pour s'initier à FastAPI et à l'intégration d’un webhook Stripe sécurisé.

**Contributions bienvenues !**

