import sqlite3

class NomLieux:
    def __init__(self, nom_lieux, description, ville):
        self.nom_lieux = nom_lieux
        self.description = description
        self.ville = ville

    def __str__(self):
        return f"NomLieux: {self.nom_lieux}, Description: {self.description}, Ville: {self.ville}"

    @staticmethod
    def item_db(listedblieux):
        """Récupère les lieux depuis la base de données."""
        connect = sqlite3.connect("listelieux.db")
        cursor = connect.cursor()
        cursor.execute("SELECT NomLieux, Description, Ville FROM NomLieux")
        rows = cursor.fetchall()
        connect.close()
        return [listedblieux(row[0], row[1], row[2]) for row in rows]


class PaireLieux:
    def __init__(self, LieuxDepart, LieuxArrivee, distance):
        self.Start = LieuxDepart
        self.end = LieuxArrivee
        self.distance = distance

    def add_db(self):
        """Ajoute une paire de lieux dans la base de données."""
        try:
            connect = sqlite3.connect("listelieux.db", timeout=10)
            cursor = connect.cursor()
            cursor.execute(
                "INSERT INTO PaireLieux (LieuxDepart, LieuxArrivee, distance) VALUES (?, ?, ?)",
                (self.Start.nom_lieux, self.end.nom_lieux, self.distance))
            connect.commit()
            print(f"Ajout réussi : {self.Start.nom_lieux} -> {self.end.nom_lieux}, Distance: {self.distance} m")
        except sqlite3.Error as e:
            print(f"Erreur SQLite : {e}")
        finally:
            if connect:
                connect.close()

    def __str__(self):
        return f"PaireLieux: {self.Start.nom_lieux} -> {self.end.nom_lieux}, Distance: {self.distance} m"

    @staticmethod
    def item_db_pairel(listedbpl):
        """Récupère les paires de lieux depuis la base de données."""
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

    def __str__(self):
        return f"Ligne: {self.NumLigne}, Sens: {self.sens}"


class TempsEntreLieux:
    def __init__(self, idTemps, HeureDebut, Heurefin, Temps, VersionTemps, PaireLieux):
        self.idTemps = idTemps
        self.HeureDebut = HeureDebut
        self.Heurefin = Heurefin
        self.temps = Temps
        self.versiontemps = VersionTemps
        self.pairelieux = PaireLieux

    def __str__(self):
        return (f"TempsEntreLieux: Début {self.HeureDebut}, Fin {self.Heurefin}, "
                f"Temps {self.temps} min, Version {self.versiontemps}")


class Composition:
    def __init__(self, IdLigne, IdpaireLieux):
        self.idligne = IdLigne
        self.idpairelieux = IdpaireLieux

    def __str__(self):
        return f"Composition: Ligne {self.idligne}, PaireLieux {self.idpairelieux}"


# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'objets NomLieux
    JUMA2 = NomLieux("jumet Madeleine", "station métro", "Jumet")
    JUCAR = NomLieux("jumet Carosse", "croisement métro", "Jumet")

    # Création d'une paire de lieux
    depart41 = PaireLieux(JUMA2, JUCAR, 833)

    # Ajout dans la base de données
    depart41.add_db()

    # Affichage des objets
    print(JUMA2)
    print(JUCAR)
    print(depart41)
