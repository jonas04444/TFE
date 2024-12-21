import sqlite3

class NomLieux:
    def __init__(self, nom_lieux, description, ville):
        self.nom_lieux = nom_lieux
        self.description = description
        self.ville = ville

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

class PaireLieux:
    def __init__(self, LieuxDepart, LieuxArrivee, distance):
        #self.idPairelieux = idPairelieux
        self.Start = LieuxDepart
        self.end = LieuxArrivee
        self.distance = distance

    def add_db(self):
        connect = None
        try:
            connect = sqlite3.connect("listelieux.db", timeout=10)
            cursor = connect.cursor()
            cursor.execute(
                "INSERT INTO PaireLieux (LieuxDepart, LieuxArrivee, distance) VALUES (?, ?, ?)",
                (self.Start.nom_lieux, self.end.nom_lieux, self.distance))
            connect.commit()
        except sqlite3.Error as e:
            print(f"Erreur SQLite : {e}")
        finally:
            if connect:
                connect.close()
                print("Connexion SQLite fermée.")

    def item_db_pairel(listedbpl):
        connect = sqlite3.connect("listelieux.db")
        cursor = connect.cursor()
        cursor.execute("SELECT IDPaireLieux, LieuxDepart, LieuxArrivee FROM PaireLieux")
        rows = cursor.fetchall()
        connect.close()
        return [listedbpl(row[0], row[1], row[2]) for row in rows]

class Ligne:
    def __init__(self, idLigne, NumLigne, Sens):
        self.idLigne = idLigne
        self.NumLigne = NumLigne
        self.sens = Sens

class TempsEntreLieux:
    def __init__(self, idTemps, HeureDebut, Heurefin, Temps, VersionTemps, PaireLieux):
        self.idTemps = idTemps
        self.HeureDebut = HeureDebut
        self.Heurefin = Heurefin
        self.temps = Temps
        self.versiontemps = VersionTemps
        self.pairelieux = PaireLieux

class Composition:
    def __init__(self, IdLigne, IdpaireLieux):
        self.idligne = IdLigne
        self.idpairelieux = IdpaireLieux

