from pymongo import MongoClient

# Connexion au serveur MongoDB local
client = MongoClient("mongodb://localhost:27017/")

# Créer/accéder à une base de données
db = client["pointing_game"]

# Créer/accéder à une collection
collection = db["joueurs"]

# Insérer un document test
collection.insert_one({"joueur": "test", "score": 0})

# Lire tous les documents
for doc in collection.find():
    print(doc)

print("Connexion réussie !")