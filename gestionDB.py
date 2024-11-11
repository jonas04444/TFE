import sqlite3
from main import *

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
