from pymongo import MongoClient
from datetime import datetime
from tkinter import messagebox

client = MongoClient("mongodb://localhost:27017/")
db = client["pointing_game"]
collection_parties = db["parties"]



def sauvegarder_partie(config):
    """Sauvegarde l'état complet pour permettre une reprise ultérieure"""
    
    if config.score_j1 > config.score_j2:
        gagnant = config.j1
    elif config.score_j2 > config.score_j1:
        gagnant = config.j2
    else:
        gagnant = "Égalité"

    try:
        collection_parties.insert_one({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "joueur1": config.j1,
            "joueur2": config.j2,
            "score_j1": config.score_j1,
            "score_j2": config.score_j2,
            "n": config.n,             
            "grille": config.grille,  
            "joueur_actuel": config.joueur_actuel,
            "gagnant": gagnant,
            "alignements": config.alignements
        })
    except Exception as e:
        print(f"Erreur DB : {e}")


def get_historique():
    try:
        return list(collection_parties.find().sort("date", -1))
    except Exception as e:
        print(f"Erreur de lecture : {e}")
        return []

def tester_connexion():
    """Vérifie si MongoDB est accessible au démarrage."""
    try:
        client.admin.command('ping')
        return True
    except Exception:
        return False
    
def mettre_a_jour_partie(config):
    """Met à jour la partie existante au lieu d'en créer une nouvelle"""
    if config.score_j1 > config.score_j2:
        gagnant = config.j1
    elif config.score_j2 > config.score_j1:
        gagnant = config.j2
    else:
        gagnant = "Égalité"

    try:
        collection_parties.update_one(
            {"_id": config.partie_id},  
            {"$set": {
                "score_j1": config.score_j1,
                "score_j2": config.score_j2,
                "grille": config.grille,
                "joueur_actuel": config.joueur_actuel,
                "gagnant": gagnant
            }}
        )
    except Exception as e:
        print(f"Erreur update : {e}")