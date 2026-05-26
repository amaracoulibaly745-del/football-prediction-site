import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import os

st.set_page_config(
    page_title="⚽ Football Prediction",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("⚽ Football Match Prediction")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Sélectionner une page:",
        ["🏠 Accueil", "🔮 Prédictions", "📊 Statistiques", "👨‍⚖️ Arbitres", "📈 Analytics"]
    )

if page == "🏠 Accueil":
    st.header("Bienvenue sur Football Prediction")
    st.markdown("""
    ### ⚽ À propos
    
    Ce site utilise l'intelligence artificielle et l'analyse de données pour prédire 
    les résultats des matchs de football avec une grande précision.
    
    ### 📊 Nos données
    - Historique complète des matchs
    - Statistiques des équipes
    - Performance des joueurs
    - Analyse des arbitres
    - Conditions de jeu
    
    ### 🤖 Notre technologie
    - Machine Learning avancé
    - Analyse prédictive
    - Cloud Computing
    """)

elif page == "🔮 Prédictions":
    st.header("Prédictions de Matchs")
    
    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("Équipe 1:", ["Manchester United", "Liverpool", "Arsenal", "Chelsea"])
    with col2:
        team2 = st.selectbox("Équipe 2:", ["Manchester City", "Real Madrid", "Barcelona", "Bayern Munich"])
    
    match_date = st.date_input("Date du match:", datetime.now() + timedelta(days=7))
    referee = st.selectbox("Arbitre (optionnel):", ["Aucun", "André Marriner", "Michael Oliver"], index=0)
    
    if st.button("🔮 Faire une prédiction", use_container_width=True):
        st.info("Prédiction en cours...")
        # Appel à l'API
        try:
            response = requests.post(
                f"{BACKEND_URL}/predict",
                json={
                    "team1": team1,
                    "team2": team2,
                    "date": str(match_date),
                    "referee": referee if referee != "Aucun" else None
                }
            )
            if response.status_code == 200:
                prediction = response.json()
                st.success("Prédiction complétée!")
                st.json(prediction)
        except Exception as e:
            st.error(f"Erreur: {str(e)}")

elif page == "📊 Statistiques":
    st.header("Statistiques des Équipes")
    st.info("Les statistiques seront chargées depuis la base de données")
    
elif page == "👨‍⚖️ Arbitres":
    st.header("Analyse des Arbitres")
    st.markdown("""
    ### Impact des arbitres sur les matchs
    
    Analyse complète de l'influence des arbitres incluant:
    - Moyenne de cartons par match
    - Moyenne de pénalties accordés
    - Tendances décisionnelles
    - Performance par équipe
    """)
    
elif page == "📈 Analytics":
    st.header("Analytics Avancées")
    st.info("Dashboards et visualisations détaillées")

st.markdown("---")
st.markdown("© 2024 Football Prediction. Tous droits réservés.")
