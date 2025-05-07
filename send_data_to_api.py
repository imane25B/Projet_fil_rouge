import requests
import json
import time
from tqdm import tqdm

# URL de ton API FastAPI
API_URL = "http://localhost:8000/heros"  # Point de terminaison pour ajouter des héros
HEADERS = {
    "token": "mytoken123",  # Envoyer directement le token sans "Bearer"
}

# Fonction pour lire les données depuis un fichier JSON
def read_json_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# Fonction pour transformer les données
def transform_data(data):
    transformed_data = []
    for org in data:
        # Exemple de transformation des données (ajouter un champ "avis")
        if org.get("score", 0) > 50:
            org["avis"] = "positif"
        else:
            org["avis"] = "négatif"

        # Supprimer des clés inutiles
        keys_to_remove = [
            "ntee_code", "raw_ntee_code", "subseccd", "has_subseccd", 
            "have_filings", "have_extracts", "have_pdfs"
        ]
        for key in keys_to_remove:
            if key in org:
                del org[key]

        # Renommer certains champs
        if "name" in org:
            org["nom"] = org["name"]
            del org["name"]
        
        if "city" in org:
            org["saga"] = org["city"]
            del org["city"]
        
        # Ajouter à la liste transformée
        transformed_data.append(org)
    
    return transformed_data

# Fonction pour envoyer les données à l'API via POST
def send_to_api(data):
    for org in tqdm(data, desc="Envoi des données", unit="organisme"):
        try:
            response = requests.post(API_URL, json=org, headers=HEADERS)
            
            # Gérer les réponses du serveur
            if response.status_code == 200:
                result = f"✅ Succès : Données envoyées pour {org['nom']}"
            elif response.status_code == 401:
                result = f"⛔ Échec : Ce héros existe déjà - {org['nom']}"
            else:
                result = f"⛔ Échec : Erreur {response.status_code} pour {org['nom']}"
            
            # Log des résultats
            log_results(result)
        
        except requests.exceptions.RequestException as e:
            result = f"⚠️ Erreur réseau : {e} pour {org['nom']}"
            log_results(result)
        
        # Temps de pause pour éviter de surcharger l'API
        time.sleep(0.5)

# Fonction pour loguer les résultats dans un fichier
def log_results(result, filename="log.txt"):
    with open(filename, "a", encoding="utf-8") as log_file:
        log_file.write(result + "\n")

# Fonction principale
def main():
    # Lire les données depuis le fichier JSON
    data = read_json_file("resultats.json")
    
    # Transformer les données
    transformed_data = transform_data(data)
    
    # Envoyer les données à l'API
    send_to_api(transformed_data)

if __name__ == "__main__":
    main()
