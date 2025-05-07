import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

# Configuration de l'API
API_BASE_URL = "http://localhost:8000"
TOKEN_API = "mytoken123"

# Titre de l'application
st.set_page_config(page_title="Gestion des Héros SF", layout="wide")
st.title("🦸 Système de Gestion des Héros de Science-Fiction")

# Sidebar pour la navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisir une section", [
    "Explorateur des Héros", 
    "Ajout via Webhook", 
    "Traitement des Données",
    "Gestion des Abonnements"
])

# Fonctions utilitaires
def call_api(endpoint, method="GET", json_data=None):
    headers = {"token": TOKEN_API}
    try:
        if method == "GET":
            response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
        else:
            response = requests.post(
                f"{API_BASE_URL}{endpoint}", 
                headers=headers, 
                json=json_data
            )
        return response.json() if response.status_code == 200 else {"error": response.text}
    except Exception as e:
        return {"error": str(e)}

# Page 1: Explorateur des Héros
if page == "Explorateur des Héros":
    st.header("📜 Liste des Héros")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Rafraîchir la liste"):
            with st.spinner("Chargement des héros..."):
                data = call_api("/heros")
                if "error" not in data:
                    st.session_state.heros = data
    
    with col2:
        search_term = st.text_input("Rechercher par nom")
    
    if "heros" in st.session_state:
        df = pd.DataFrame(st.session_state.heros)
        
        if search_term:
            df = df[df["nom"].str.contains(search_term, case=False)]
        
        st.dataframe(df, use_container_width=True)
        
        st.download_button(
            label="Télécharger en JSON",
            data=json.dumps(st.session_state.heros, indent=2, ensure_ascii=False),
            file_name=f"heros_sf_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    else:
        st.info("Cliquez sur 'Rafraîchir la liste' pour charger les héros")

# Page 2: Ajout via Webhook
elif page == "Ajout via Webhook":
    st.header("🤖 Ajout via Webhook")
    
    with st.form("webhook_form"):
        nom = st.text_input("Nom du personnage", "Naruto")
        score = st.slider("Score", 0, 100, 85)
        
        if st.form_submit_button("Envoyer au Webhook"):
            data = {"nom": nom, "score": score}
            result = call_api("/webhook/personnage", "POST", data)
            
            if "error" not in result:
                st.success(f"✅ {result['message']}")
                st.json(result)
            else:
                st.error(f"Erreur: {result['error']}")

# Page 3: Traitement des Données
elif page == "Traitement des Données":
    st.header("⚙️ Traitement des Données")
    
    uploaded_file = st.file_uploader("Choisir un fichier JSON", type=["json"])
    
    if uploaded_file:
        data = json.load(uploaded_file)
        st.info(f"{len(data)} entrées chargées")
        
        if st.button("Lancer le traitement"):
            progress_bar = st.progress(0)
            results = []
            
            for i, item in enumerate(data):
                # Pour le format webhook_log.json
                if "personnage" in item:
                    payload = item["personnage"]
                else:
                    payload = item
                
                response = call_api("/traitement", "POST", payload)
                
                if "error" not in response:
                    results.append(response)
                
                progress_bar.progress((i + 1) / len(data))
            
            st.success(f"Traitement terminé ({len(results)}/{len(data)} succès)")
            
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
            
            st.download_button(
                label="Télécharger les résultats",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="resultats_traitement.csv",
                mime="text/csv"
            )

# Page 4: Gestion des Abonnements
elif page == "Gestion des Abonnements":
    st.header("🔔 Gestion des Notifications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Statut actuel")
        status = st.radio("Notifications", ["Activées", "Désactivées"], index=0)
        
        if st.button("Appliquer"):
            result = call_api(f"/subscribe/{'on' if status == 'Activées' else 'off'}", "POST")
            st.session_state.notif_status = status
            st.success(f"Notifications {status.lower()}")

    with col2:
        st.subheader("Journal des notifications")
        if st.button("Voir le journal"):
            try:
                with open("notifications.txt", "r", encoding="utf-8") as f:
                    logs = f.readlines()
                
                if logs:
                    st.text_area("Dernières notifications", "\n".join(logs[-10:]), height=200)
                else:
                    st.info("Aucune notification enregistrée")
            except FileNotFoundError:
                st.warning("Aucun fichier de log trouvé")