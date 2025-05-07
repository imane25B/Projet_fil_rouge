import requests
import json
import time

BASE_URL = "https://projects.propublica.org/nonprofits/api/v2/search.json"
QUERY = "chat"
OUTPUT_FILE = "resultats.json"
HEADERS = {"User-Agent": "Mozilla/5.0"}  # Pour éviter d'être bloqué

def extract(query):
    page = 0
    all_results = []

    while True:
        try:
            print(f"🔄 Récupération page {page}...")
            response = requests.get(BASE_URL, params={"q": query, "page": page}, headers=HEADERS, timeout=10)
            
            if response.status_code != 200:
                print(f"⛔ Erreur HTTP {response.status_code} à la page {page}")
                break

            data = response.json()
            organizations = data.get("organizations", [])
            print(organizations)
            if not organizations:
                print("✅ Fin de la pagination.")
                break

            all_results.extend(organizations)
            page += 1
            time.sleep(1)  # Anti-spam API

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Erreur réseau : {e}")
            break

    return all_results

def transform(data):
    filtered = []
    total_score = 0
    count = 0

    for org in data:
        score = org.get("score", 0)
        city = org.get("city")
        if city and score and score > 70:
            filtered.append(org)
            total_score += score
            count += 1

    moyenne = total_score / count if count else 0
    print(f"📊 Moyenne des scores filtrés : {round(moyenne, 2)}")
    return filtered

def load(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Données sauvegardées dans '{filename}'")
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier : {e}")

def main():

    """
    Exécute l'extraction, la transformation et la sauvegarde des données.

    1. Extrait les données à l'aide de l'API ProPublica.
    2. Transforme et filtre les données.
    3. Sauvegarde les données filtrées dans un fichier JSON.
    """
    raw_data = extract(QUERY)
    filtered_data = transform(raw_data)
    load(filtered_data, OUTPUT_FILE)

if __name__ == "__main__":
    main()
