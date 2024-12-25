import sqlite3
from itertools import count
from tkinter import messagebox

def new_table():
    connect = sqlite3.connect("user.db")
    quest = connect.cursor()
    quest.execute("""CREATE TABLE Graphiqueur (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        identifiant TEXT,
        password INTEGER)
        """)
    connect.close()

def add_user(log, password):
    connect = sqlite3.connect("user.db")
    quest = connect.cursor()
    quest.execute("INSERT INTO Graphiqueur (identifiant, password) VALUES (?, ?)", (log, password))
    connect.commit()
    connect.close()

def add_lieux(IDLieux, Description, Ville):
    if not IDLieux or not Description or not Ville:
        messagebox.showerror("ERREUR", "Veuillez remplir tous les champs.")
    else:
        #print(f"IDLieux: {IDLieux}, Description: {Description}, Ville: {Ville}")
        connect = sqlite3.connect("listelieux.db")
        quest = connect.cursor()
        quest.execute("INSERT INTO NomLieux ("
                      "NomLieux, Description, "
                      "Ville) VALUES (?, ?, ?)",
                      (IDLieux, Description,Ville))
        connect.commit()
        connect.close()

def add_duo_lieux(lieux_start, Lieux_end, Distance):
    if not lieux_start or not Lieux_end or not Distance:
        messagebox.showerror("ERREUR", "Veuillez remplir tous les champs.")
    else:
        try:
            connect = sqlite3.connect("listelieux.db")
            cursor = connect.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM PaireLieux WHERE LieuxDepart= ? AND LieuxArrivee=?",
                (lieux_start, Lieux_end)
            )
            countPL = cursor.fetchone()[0]

            if countPL > 0:
                messagebox.showerror("ERREUR", "La paire de lieux existe déjà.")
            else:
                cursor.execute(
                    "INSERT INTO PaireLieux (LieuxDepart, LieuxArrivee, distance) VALUES (?, ?, ?)",
                    (lieux_start, Lieux_end, Distance))
                connect.commit()
                messagebox.showinfo("VALIDE", "Paire de lieux ajoutée")
        except sqlite3.Error:
            print("Erreur Pairelieux")

        finally:
            if connect:
             connect.close()

def add_temps_parcours(HStart,HEnd,Temps,VersionT,LieuxDepart, LieuxArrivee):
    if not HStart or not HEnd or not Temps or not VersionT or not LieuxDepart or not LieuxArrivee:
        messagebox.showerror("ERREUR", "Veuillez remplir tous les champs.")
    else:
        try:
            connect = sqlite3.connect("listelieux.db")
            cursor = connect.cursor()
            cursor.execute(
                "SELECT idPaireLieux FROM PaireLieux WHERE LieuxDepart = ? AND LieuxArrivee = ?",
                (LieuxDepart, LieuxArrivee)
            )
            result = cursor.fetchone()
            #print("test1")
            if result:
                idpairelieux = result[0]
            else:
                print("paire de lieux n'existe pas")
                return
            #print(idpairelieux)
            cursor.execute(
                "SELECT COUNT(*) FROM TempsEntreLieux WHERE (HeureDebut = ? OR HeureFin = ?) AND VersionTemps = ? AND PaireLieux = ?",
                (HStart,HEnd,VersionT, idpairelieux)
            )
            #print("test2")
            countVPL = cursor.fetchone()[0]

            if countVPL > 0:
                messagebox.showerror("ERREUR","il y a déjà une version de temps pour ce lieux")
            else:
                cursor.execute(
                    "INSERT INTO TempsEntreLieux (HeureDebut, HeureFin, Temps, VersionTemps, PaireLieux) "
                    "VALUES (?, ?, ?, ?, ?)", (HStart,HEnd,Temps,VersionT,idpairelieux))
                connect.commit()
                messagebox.showinfo("VALIDE", "Temps de parcrous entre lieux ajouté")
        except sqlite3.Error as error:
            print(f"Erreur temps entre lieux : {error}")
        finally:
            if connect:
                connect.close()

def Creer_ligne (Num_Ligne, Sens):
    if not Num_Ligne or not Sens:
        messagebox.showerror("ERREUR", "Veuilllez remplis tous les champs.")
    else:
        try:
            connect = sqlite3.connect("listelieux.db")
            cursor = connect.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM Ligne WHERE NumLigne = ? AND Sens = ?",
                (Num_Ligne,Sens)
            )
            countLigne = cursor.fetchone()[0]

            if countLigne > 0:
                messagebox.showerror("ERREUR","cette ligne existe déjà")
            else:
                cursor.execute(
                    "INSERT INTO Ligne (NumLigne , Sens) Values (?,?) ",
                    (Num_Ligne,Sens))
                connect.commit()
                messagebox.showinfo("VALIDE","la ligne a bien été créée")
        except sqlite3.Error as error:
            print(f"Erreur ligne de bus : {error}")
        finally:
            if connect:
                connect.close()

#test = add_temps_parcours("0:00", "6:00", 2, "C0041", "JUMA2", "JUCAR")
