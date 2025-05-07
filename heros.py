import sqlite3
import json

# Liste des héros par défaut
heros_par_defaut = [
    {"nom": "Luke Skywalker", "saga": "Star Wars"},
    {"nom": "Paul Atreides", "saga": "Dune"},
    {"nom": "Ellen Ripley", "saga": "Alien"},
    {"nom": "Spock", "saga": "Star Trek"},
    {"nom": "Neo", "saga": "Matrix"}
]

# Nom du fichier de la base de données SQLite
db_filename = "heros_sf.db"

# Connexion à la base de données SQLite
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Création de la table si elle n'existe pas déjà
cursor.execute('''
    CREATE TABLE IF NOT EXISTS heros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        saga TEXT NOT NULL
    )
''')

# Insertion des héros par défaut dans la base de données
for hero in heros_par_defaut:
    cursor.execute('''
        INSERT INTO heros (nom, saga) VALUES (?, ?)
    ''', (hero['nom'], hero['saga']))

# Sauvegarde des changements et fermeture de la connexion à la base de données
conn.commit()
conn.close()

# Création du fichier JSON avec le nom "heros.json"
json_filename = "heros_sf.json"

# Sauvegarde des héros dans le fichier JSON
with open(json_filename, "w", encoding="utf-8") as fichier:
    json.dump(heros_par_defaut, fichier, ensure_ascii=False, indent=2)

print(f"Les fichiers '{db_filename}' et '{json_filename}' ont été créés avec succès.")
