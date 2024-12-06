import sqlite3
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
        #print(f"IDLieux: {lieux_start}, Description: {Lieux_end}, Ville: {Distance}")
        connect = sqlite3.connect("PaireLieux.db")
        quest = connect.cursor()
        quest.execute("INSERT INTO PaireLieux ("
                      "LieuxDepart, LieuxArrivee, "
                      "distance) VALUES (?, ?, ?)",
                      (lieux_start, Lieux_end,Distance))
        connect.commit()
        connect.close()
