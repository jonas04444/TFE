import sqlite3

class NomLieux:
    def __init__(self, nom_lieux: str, description: str, ville: str):
        self.nom_lieux = nom_lieux
        self.description = description
        self.ville = ville

    def item_db(self):
        connect = sqlite3.connect("listelieux.db")
        cursor = connect.cursor()
        cursor.execute("SELECT NomLieux, Description, Ville FROM NomLieux")
        rows = cursor.fetchall()
        connect.close()
        return [self(row[0], row[1], row[2]) for row in rows]

    def addlieux(self):
        try:
            connect = sqlite3.connect("listelieux.db")
            cursor = connect.cursor()
            cursor.execute("SELECT COUNT(*) FROM NomLieux WHERE NomLieux = ?", (self.nom_lieux))
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

        except sqlite3.Error:
            print("Erreur Lieux")

        finally:
            connect.close()

class PaireLieux:
    def __init__(self, LieuxDepart, LieuxArrivee, distance: int):
        self.idPairelieux = None
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
            #récupérer la clés
            idPairelieux = cursor.lastrowid
            connect.commit()
            print("paire de lieux ajoutée")
            print(idPairelieux)
            return idPairelieux
        except sqlite3.Error as e:
            print("Erreur Pairelieux")
        finally:
            if connect:
                connect.close()
                print("Connexion fermée.")

    def item_db_pairel(listedbpl):
        connect = sqlite3.connect("listelieux.db")
        cursor = connect.cursor()
        cursor.execute("SELECT IDPaireLieux, LieuxDepart, LieuxArrivee FROM PaireLieux")
        rows = cursor.fetchall()
        connect.close()
        return [listedbpl(row[0], row[1], row[2]) for row in rows]

    def __repr__(self):
        return f"PaireLieux(Start={self.Start.nom_lieux}, End={self.end.nom_lieux}, Distance={self.distance})"

class Ligne:
    def __init__(self, idLigne: int, NumLigne: int, Sens: str):
        self.idLigne = idLigne
        self.NumLigne = NumLigne
        self.sens = Sens

class TempsEntreLieux:
    def __init__(self, HeureDebut: str, Heurefin: str, Temps: int, VersionTemps: str, PaireLieux):
        self.HeureDebut = HeureDebut
        self.Heurefin = Heurefin
        self.temps = Temps
        self.versiontemps = VersionTemps
        self.pairelieux = PaireLieux

    def add_dbtemp(self):
        connect = None
        try:
            connect = sqlite3.connect("listelieux.db", timeout=10)
            cursor = connect.cursor()
            cursor.execute(
                "SELECT idPaireLieux FROM PaireLieux WHERE LieuxDepart = ? AND LieuxArrivee = ?",
                (self.pairelieux.Start.nom_lieux, self.pairelieux.end.nom_lieux)
            )
            result = cursor.fetchone()
            if result:
                idpairelieux = result[0]
            else:
                print("paire de lieux n'existe pas")
                return

            cursor.execute(
                "INSERT INTO TempsEntreLieux (HeureDebut, Heurefin, temps, versiontemps, pairelieux) "
                "VALUES (?, ?, ?, ?, ?)",
                (self.HeureDebut, self.Heurefin, self.temps, self.versiontemps, idpairelieux)
            )
            connect.commit()
            print("Temps entre lieux ajouté")
        except sqlite3.Error:
            print("Erreur temp")
        finally:
            if connect:
                connect.close()
                print("Connexion fermée.")


class Composition:
    def __init__(self, IdLigne):
        self.idligne = IdLigne
        self.idpairelieux = []

    def addpairelieux(self, pairelieux):
        self.idpairelieux.append(pairelieux)

ligne41 = Ligne(141,41,"aller")

JUMA2 = NomLieux("JUMA2", "test","jumet")
JUCAR = NomLieux("JUCAR", "test 2", "Jumet")
GOCAL = NomLieux("GOCAL","calvaire","gosselies")
AAAA= NomLieux("AAAAA", "test", "test")

JUMA2JUCAR = PaireLieux(JUMA2,JUCAR,833)
JUCARGOCAL = PaireLieux(JUCAR,GOCAL,979)

#JUMA2JUCAR.add_db()
TEST = Composition(ligne41)
#TEST.addpairelieux(JUCARGOCAL)

TJUMA2JUCAR = TempsEntreLieux("0:00", "6:59", 2, "C0041", JUMA2JUCAR)
TJUMA2JUCAR.add_dbtemp()



