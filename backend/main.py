from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

app = FastAPI(
    title="Football Prediction API",
    description="API pour les prédictions de football",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Football Prediction API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Health endpoint"""
    return {"status": "healthy"}

@app.post("/predict")
async def predict_match(match_data: dict):
    """
    Prédire le résultat d'un match
    
    match_data: {
        "team1": str,
        "team2": str,
        "date": str,
        "referee": str (optional)
    }
    """
    logger.info(f"Prediction request for {match_data}")
    return {
        "prediction": "In progress",
        "confidence": 0.0
    }

@app.get("/teams")
async def get_teams():
    """Récupérer la liste des équipes"""
    return {"teams": []}

@app.get("/referees")
async def get_referees():
    """Récupérer les statistiques des arbitres"""
    return {"referees": []}

@app.get("/matches/{match_id}")
async def get_match(match_id: str):
    """Récupérer les détails d'un match"""
    return {"match_id": match_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("BACKEND_HOST", "0.0.0.0"),
        port=int(os.getenv("BACKEND_PORT", 8000))
    )
