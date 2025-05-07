import requests
import json
from tqdm import tqdm

# Configuration
API_URL = "http://localhost:8000/traitement"
FICHIER_ENTREE = "personnages.json" 
FICHIER_SORTIE = "personnages_enrichis.json"

def charger_personnages():
    """Charge les personnages depuis le fichier JSON"""
    with open(FICHIER_ENTREE, "r", encoding="utf-8") as f:
        return json.load(f)

def traiter_personnages(personnages):
    """Envoie chaque personnage à l'API pour traitement"""
    resultats = []
    for p in tqdm(personnages, desc="Traitement des personnages"):
        try:
            response = requests.post(API_URL, json=p)
            if response.status_code == 200:
                resultats.append(response.json())
                print(f"{p['nom']} -> Niveau: {response.json()['niveau']}")
            else:
                print(f"Erreur pour {p['nom']}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur réseau pour {p['nom']}: {str(e)}")
    return resultats

def sauvegarder_resultats(resultats):
    """Sauvegarde les résultats enrichis"""
    with open(FICHIER_SORTIE, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

def main():
    # 1. Charger les données
    personnages = charger_personnages()
    print(f"⏳ {len(personnages)} personnages à traiter")
    
    # 2. Traiter via l'API
    personnages_enrichis = traiter_personnages(personnages)
    
    # 3. Sauvegarder les résultats
    sauvegarder_resultats(personnages_enrichis)
    print(f"✅ Résultats sauvegardés dans {FICHIER_SORTIE}")
    print(f"Résumé: {len(personnages_enrichis)} personnages traités")

if __name__ == "__main__":
    main()