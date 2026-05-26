# ⚽ Football Prediction Site

Site de prédiction de football basé sur l'analyse de données complètes incluant les équipes, joueurs, historique de matchs et arbitres.

## 🎯 Objectifs

- Prédire les résultats des matchs de football
- Analyser l'impact des arbitres sur les matchs
- Fournir des statistiques détaillées et visualisations
- Interface utilisateur intuitive et moderne

## 🏗️ Architecture

```
football-prediction-site/
├── backend/                 # API FastAPI
├── ml/                      # Models de machine learning
├── data/                    # Pipeline de collecte de données
├── frontend/                # Interface Streamlit
├── cloud/                   # Configuration cloud (Firebase, etc.)
├── config/                  # Configuration centralisée
├── tests/                   # Tests unitaires
├── requirements.txt         # Dépendances Python
├── docker-compose.yml       # Orchestration Docker
└── .env.example             # Variables d'environnement
```

## 📋 Stack Technologique

- **Backend** : FastAPI
- **ML/Data** : scikit-learn, pandas, numpy
- **Frontend** : Streamlit
- **Cloud** : Firebase (Firestore + Authentication)
- **Base de données** : Firestore
- **Containerization** : Docker

## 🚀 Démarrage Rapide

### 1. Cloner le repository
```bash
git clone https://github.com/amaracoulibaly745-del/football-prediction-site.git
cd football-prediction-site
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration Cloud
```bash
cp .env.example .env
# Configurer vos credentials Firebase
```

### 4. Lancer le projet
```bash
# Backend
cd backend && python main.py

# Frontend (dans un autre terminal)
cd frontend && streamlit run app.py
```

## 📊 Données Utilisées

- **Équipes** : Performances, historique
- **Joueurs** : Form, statistiques, blessures
- **Arbitres** : Historique de décisions, tendances
- **Matchs** : Résultats historiques, contexte
- **Conditions** : Météo, terrain, domicile/extérieur

## 🤖 Modèles ML

- Prédiction du score final
- Prédiction des statistiques (corners, cartons, etc.)
- Analyse d'impact arbitre
- Probabilités de résultats (victoire/nul/défaite)

## 🔗 APIs Utilisées

- [Rapid API - Football API](https://rapidapi.com/api-sports/api/api-football)
- [ESPN Data](https://www.espn.com/apis)
- [Flashscore](https://www.flashscore.com/)

## 📝 Licence

MIT
