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

def confirm_user(nomuser, password):
    connect = sqlite3.connect("user.db")
    quest = connect.cursor()
    try:
        quest.execute("SELECT identifiant FROM Graphiqueur WHERE identifiant = ? AND password = ?", (nomuser, password))
        utilisateur = quest.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Erreur Base de Données", f"Erreur lors de la connexion : {e}")
    finally:
        quest.close()
        connect.close()

    if utilisateur:
        graph_select()
        print("Utilisateur trouvé :", utilisateur)
    else:
        messagebox.showerror("ERREUR", "Nom d'utilisateur ou mot de passe incorrect")

def add_lieux(IDLieux, Description, Ville):
    if not IDLieux or not Description or not Ville:
        messagebox.showerror("ERREUR", "Veuillez remplir tous les champs.")
    else:
        print(f"IDLieux: {IDLieux}, Description: {Description}, Ville: {Ville}")
        connect = sqlite3.connect("listelieux.db")
        quest = connect.cursor()
        quest.execute("INSERT INTO NomLieux ("
                      "NomLieux, Description, "
                      "Ville) VALUES (?, ?, ?)",
                      (IDLieux, Description,Ville))
        connect.commit()
        connect.close()



