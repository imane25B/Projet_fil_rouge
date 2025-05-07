from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from pydantic import BaseModel
import json
import os
import stripe
import time

# Modèle de données pour un personnage SF
class HeroSF(BaseModel):
    nom: str
    saga: str

class PersonnageWebhook(BaseModel):
    nom: str
    score: int

class PersonnageTraitement(BaseModel):
    nom: str
    score: int

class PersonnageEnrichi(PersonnageTraitement):
    niveau: str
    score_double: int
# Initialisation de l'application FastAPI
app = FastAPI(title="API Héros Science-Fiction")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet d'accepter toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales
FICHIER_HEROS = "heros_sf.json"
CLE_API = "mytoken123"
CLE_WEBHOOK_STRIPE = "whsec_abcdefgh1234567890"
FICHIER_LOG_WEBHOOK = "webhook_log.json"
ABONNES_ACTIFS = True  # Activation/désactivation globale
FICHIER_NOTIFICATIONS = "notifications.txt"

# Fonction pour lire les héros à partir du fichier JSON
def lire_heros() -> List[HeroSF]:
    if not os.path.exists(FICHIER_HEROS):
        return []
    with open(FICHIER_HEROS, "r", encoding="utf-8") as fichier:
        data = json.load(fichier)
    return [HeroSF(**item) for item in data]

# Fonction pour écrire les héros dans un fichier JSON
def ecrire_heros(heros: List[HeroSF]):
    with open(FICHIER_HEROS, "w", encoding="utf-8") as fichier:
        json.dump([h.dict() for h in heros], fichier, ensure_ascii=False, indent=2)

# Fonction de vérification de la clé API
def autoriser(token: Optional[str]):
    if token != CLE_API:
        raise HTTPException(status_code=403, detail="Clé API invalide.")

# Serveur des fichiers frontend
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

# Endpoints pour la gestion des héros
@app.get("/heros", response_model=List[HeroSF])
def lister_heros(token: Optional[str] = Header(None)):
    autoriser(token)
    return lire_heros()

@app.post("/heros", response_model=HeroSF)
def ajouter_hero(hero: HeroSF, token: Optional[str] = Header(None)):
    autoriser(token)
    heros = lire_heros()
    if any(h.nom.lower() == hero.nom.lower() for h in heros):
        raise HTTPException(status_code=401, detail="Ce héros existe déjà.")
    heros.append(hero)
    ecrire_heros(heros)
    return hero

@app.put("/heros/{nom}", response_model=HeroSF)
def modifier_hero(nom: str, donnees: HeroSF, token: Optional[str] = Header(None)):
    autoriser(token)
    heros = lire_heros()
    for i, h in enumerate(heros):
        if h.nom.lower() == nom.lower():
            heros[i] = donnees
            ecrire_heros(heros)
            return donnees
    raise HTTPException(status_code=404, detail="Héros introuvable.")

@app.delete("/heros/{nom}")
def supprimer_hero(nom: str, token: Optional[str] = Header(None)):
    autoriser(token)
    heros = lire_heros()
    nouveaux = [h for h in heros if h.nom.lower() != nom.lower()]
    if len(nouveaux) == len(heros):
        raise HTTPException(status_code=404, detail="Héros introuvable.")
    ecrire_heros(nouveaux)
    return {"message": f"Héros '{nom}' supprimé."}

@app.get("/heros/exemples", response_model=List[HeroSF])
def exemples_heros(token: Optional[str] = Header(None)):
    autoriser(token)
    return [
        HeroSF(nom="Luke Skywalker", saga="Star Wars"),
        HeroSF(nom="Paul Atreides", saga="Dune"),
        HeroSF(nom="Ellen Ripley", saga="Alien"),
        HeroSF(nom="Spock", saga="Star Trek"),
        HeroSF(nom="Neo", saga="Matrix")
    ]

def logger_webhook(personnage: dict):
    """Enregistre un personnage reçu dans le fichier de log JSON"""
    try:
        # Lire les données existantes si le fichier existe
        if os.path.exists(FICHIER_LOG_WEBHOOK):
            with open(FICHIER_LOG_WEBHOOK, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []
        
        # Ajouter le nouveau personnage avec un timestamp
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "personnage": personnage
        }
        data.append(entry)
        
        # Réécrire le fichier
        with open(FICHIER_LOG_WEBHOOK, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"⚠️ Erreur lors de l'écriture du log: {e}")

def notifier_abonnes(message: str):
    """Notifie tous les abonnés selon les canaux configurés"""
    if not ABONNES_ACTIFS:
        return
    
    # Notification console (toujours active si abonnés activés)
    print(f"🔔 Notification: {message}")
    
    # Notification fichier
    try:
        with open(FICHIER_NOTIFICATIONS, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    except Exception as e:
        print(f"❌ Erreur d'écriture dans notifications.txt: {e}")


# ---------- Nouvelle route pour l'exercice 1 - Partie 3 ----------
@app.post("/webhook/personnage")
async def recevoir_personnage(personnage: PersonnageWebhook):
    """Route pour l'exercice webhook"""
    # 1. Afficher le personnage reçu
    print(f"Webhook reçu - Nom: {personnage.nom}, Score: {personnage.score}")
    
    # 2. Enrichissement: ajout du champ niveau
    if personnage.score >= 90:
        niveau = "Légendaire"
    elif personnage.score >= 70:
        niveau = "Épique"
    elif personnage.score >= 50:
        niveau = "Rare"
    else:
        niveau = "Commun"
    
    # 3. Stocker dans heros_sf.json
    heros = lire_heros()
    nouveau_hero = HeroSF(nom=personnage.nom, saga=f"Niveau: {niveau}")
    heros.append(nouveau_hero)
    ecrire_heros(heros)
    
    # 4. [EXERCICE 3] Enregistrer dans le log webhook
    logger_webhook({
        "nom": personnage.nom,
        "score": personnage.score,
        "niveau": niveau
    })
    # Après avoir traité le personnage
    notif_message = (
        f"Nouveau personnage '{personnage.nom}' (score: {personnage.score}) "
        f"classé comme '{niveau}'"
    )
    notifier_abonnes(notif_message)
    return {
        "status": "success",
        "personnage": personnage.nom,
        "niveau": niveau,
        "message": "Personnage traité et stocké"
    }

@app.post("/subscribe/{etat}")
def gerer_abonnements(etat: str, token: Optional[str] = Header(None)):
    """
    Active/désactive les notifications pour les abonnés
    Paramètres:
        etat: 'on' pour activer, 'off' pour désactiver
    """
    autoriser(token)
    global ABONNES_ACTIFS
    
    if etat.lower() == 'on':
        ABONNES_ACTIFS = True
        message = "Notifications activées"
    elif etat.lower() == 'off':
        ABONNES_ACTIFS = False
        message = "Notifications désactivées"
    else:
        raise HTTPException(status_code=400, detail="État doit être 'on' ou 'off'")
    
    notifier_abonnes(f"Changement d'état des abonnements: {message}")
    return {"status": "success", "message": message}

@app.post("/notifier")
def route_de_notification_test(contenu: dict):
    """Route exemple pour simuler une action secondaire"""
    print(f"📢 Notification reçue: {contenu}")
    # Ici vous pourriez implémenter un système de badges, etc.
    return {"status": "notification_traitée"}

@app.post("/traitement", response_model=PersonnageEnrichi)
def traiter_personnage(personnage: PersonnageTraitement):
    """Endpoint qui enrichit les données du personnage"""
    # Calcul du niveau
    if personnage.score >= 90:
        niveau = "Légendaire"
    elif personnage.score >= 80:
        niveau = "Expert"
    elif personnage.score >= 70:
        niveau = "Avancé"
    elif personnage.score >= 50:
        niveau = "Intermédiaire"
    else:
        niveau = "Débutant"
    
    # Retour des données enrichies
    return PersonnageEnrichi(
        nom=personnage.nom,
        score=personnage.score,
        niveau=niveau,
        score_double=personnage.score * 2
    )

# Webhook Stripe pour les paiements
@app.post("/webhook/paiement")
async def stripe_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, signature, CLE_WEBHOOK_STRIPE)
    except ValueError:
        raise HTTPException(status_code=401, detail="Contenu invalide.")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=401, detail="Signature Stripe invalide.")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print(f"Paiement validé pour : {session.get('customer_email')}")

    return {"status": "traité"}
