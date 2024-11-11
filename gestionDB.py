import sqlite3
from multiprocessing.forkserver import connect_to_new_process


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
    #print(log,password)
    connect = sqlite3.connect("user.db")
    quest = connect.cursor()
    quest.execute("INSERT INTO Graphiqueur (identifiant, password) VALUES (?, ?)", (log, password))
    connect.commit()
    connect.close()

def confirm_user(nomuser,password):
    connect = sqlite3.connect("user.db")
    quest = connect.cursor()
    quest.execute("SELECT * FROM Graphiqueur")
    quest.execute("SELECT identifiant FROM Graphiqueur WHERE identifiant = ? AND password = ?", (nomuser, password))
    utilisateur = quest.fetchall()
    quest.close()
    if utilisateur:
        print(utilisateur)
    else:
        print("personne")