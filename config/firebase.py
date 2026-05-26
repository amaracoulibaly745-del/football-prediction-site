import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from loguru import logger

class FirebaseConfig:
    """
    Configuration et gestion de Firebase
    """
    
    _instance = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseConfig, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._db is None:
            self._initialize_firebase()
    
    def _initialize_firebase(self):
        """
        Initialiser Firebase avec les credentials
        """
        try:
            service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')
            
            if not service_account_path or not os.path.exists(service_account_path):
                logger.warning("Firebase service account key not found")
                return
            
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
            
            self._db = firestore.client()
            logger.info("Firebase initialized successfully")
        except Exception as e:
            logger.error(f"Firebase initialization failed: {str(e)}")
    
    @property
    def db(self):
        """Obtenir l'instance Firestore"""
        return self._db
    
    def save_prediction(self, prediction_data: dict) -> bool:
        """
        Sauvegarder une prédiction dans Firestore
        """
        try:
            self._db.collection('predictions').add(prediction_data)
            logger.info("Prediction saved to Firestore")
            return True
        except Exception as e:
            logger.error(f"Error saving prediction: {str(e)}")
            return False
    
    def get_predictions(self, limit: int = 10) -> list:
        """
        Récupérer les dernières prédictions
        """
        try:
            docs = self._db.collection('predictions').limit(limit).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            logger.error(f"Error fetching predictions: {str(e)}")
            return []
    
    def save_match_data(self, match_data: dict) -> bool:
        """
        Sauvegarder les données d'un match
        """
        try:
            self._db.collection('matches').add(match_data)
            return True
        except Exception as e:
            logger.error(f"Error saving match data: {str(e)}")
            return False
