import sqlite3

class NomLieux:
    def __init__(self, nom_lieux, description, ville):
        self.nom_lieux = nom_lieux
        self.description = description
        self.ville = ville

    @staticmethod
    def item_db(listedblieux):
        connect = sqlite3.connect("listelieux.db")
        cursor = connect.cursor()
        cursor.execute("SELECT NomLieux, Description, Ville FROM NomLieux")
        rows = cursor.fetchall()
        connect.close()
        return [listedblieux(row[0], row[1], row[2]) for row in rows]

    def addlieux(self):
        try:
            connect = sqlite3.connect("listelieux.db")
            cursor = connect.cursor()
            cursor.execute("SELECT COUNT(*) FROM NomLieux WHERE NomLieux = ?", (self.nom_lieux,))
            count = cursor.fetchone()[0]

            if count > 0:
                print(f"Le lieu {self.nom_lieux} existe déjà.")
            else:
                cursor.execute(
                    "INSERT INTO NomLieux (NomLieux, Description, Ville) VALUES (?, ?, ?)",
                    (self.nom_lieux, self.description, self.ville)
                )
                connect.commit()
                print("lieux ajouté")

        except sqlite3.Error as e:
            print(f"Erreur de connexion: {e}")

        finally:
            connect.close()


def create_table():
    try:
        conn = sqlite3.connect("listelieux.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS NomLieux (
                NomLieux TEXT PRIMARY KEY,
                Description TEXT,
                Ville TEXT
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la table : {e}")
    finally:
        conn.close()

JUMA2 = NomLieux("JUMA2", "station métro", "Jumet")
JUCAR = NomLieux("JUCAR", "croisement métro", "Jumet")

AAAAA = NomLieux("AAAAA", "test", "ici")


