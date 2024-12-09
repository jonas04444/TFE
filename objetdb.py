import sqlite3

class NomLieux:
    def __init__(self, nom_lieux, description, ville):
        self.nom_lieux = nom_lieux
        self.description = description
        self.ville = ville

    def item_db(listedb):
        connect = sqlite3.connect("listelieux.db")
        cursor = connect.cursor()
        cursor.execute("SELECT NomLieux, Description, Ville FROM NomLieux")
        rows = cursor.fetchall()
        return [listedb(row[0], row[1], row[2]) for row in rows]
