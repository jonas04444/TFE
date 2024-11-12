import tkinter as Tk
from tkinter import messagebox
import sqlite3

def graph_select():
    win = Tk.Toplevel(root)
    win.title("Section")
    win.geometry("500x500")

    login_graph_select = Tk.Label(win, textvariable=login_name)
    login_graph_select.pack()

    button_generate = Tk.Button(win, text="Générer tableau comparatif")
    button_generate.pack()
    button_add_date = Tk.Button(win, text="Ajouter ou modifier des données")
    button_add_date.pack()
    button_view_data = Tk.Button(win, text="Voir des données")
    button_view_data.pack()

def visitor():
    win_visitor = Tk.Toplevel(root)
    win_visitor.title("Voir des données")

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


root = Tk.Tk()
root.title("Analyse temps de parcours")
root.geometry("600x600")

title = Tk.Label(root, text="Analyse de temps de parcours", font=("Arial", 25))
title.pack()

login = Tk.Label(root, text="Entrez votre identifiant")
login.pack()

login_name = Tk.StringVar()
name_entry = Tk.Entry(root, textvariable=login_name)
name_entry.focus_set()
name_entry.pack()

password_label = Tk.Label(root, text="Entrez votre mot de passe")
password_label.pack()

password_log = Tk.StringVar()
password_entry = Tk.Entry(root, textvariable=password_log, show="*")
password_entry.pack()

button_connect = Tk.Button(root, text="Connexion", width=30, height=3, command=lambda: confirm_user(login_name.get(), password_log.get()))
button_connect.pack()

button_visitor = Tk.Button(root, text="Se connecter en tant que visiteur", width=30, height=3, command=visitor)
button_visitor.pack()

root.mainloop()
