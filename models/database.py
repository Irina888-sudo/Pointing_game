from pymongo import MongoClient
from datetime import datetime
from tkinter import messagebox

client = MongoClient("mongodb://localhost:27017/")
db = client["pointing_game"]
collection_parties = db["parties"]


def sauvegarder_partie(nom1, nom2, score_j1, score_j2):
    """Sauvegarde le résultat d'une partie"""
    if score_j1 > score_j2:
        gagnant = nom1
    elif score_j2 > score_j1:
        gagnant = nom2
    else:
        gagnant = "Égalité"
    try:
     collection_parties.insert_one({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "joueur1": nom1,
        "joueur2": nom2,
        "score_j1": score_j1,
        "score_j2": score_j2,
        "gagnant": gagnant
    
    })
    except Exception as e:
        
        print(f"Erreur DB : {e}")
        messagebox.showwarning("Base de données", "Impossible de sauvegarder le score.")


def get_historique():
    """Retourne toutes les parties jouées"""
    return list(collection_parties.find().sort("date", -1))


def tester_connexion():
    """Vérifie si MongoDB est accessible au démarrage."""
    try:
        client.admin.command('ping')
        return True
    except Exception:
        return False