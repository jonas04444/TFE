import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def graph_select():
    ConDB = sqlite3.connect("listelieux.db")
    cursor = ConDB.cursor()

    cursor.execute("SELECT * FROM NomLieux")
    rows = cursor.fetchall()

    win = tk.Toplevel(root)
    win.title("Section")
    win.geometry("500x500")

    login_graph_select = tk.Label(win, textvariable=login_name)
    login_graph_select.pack()

    button_generate = tk.Button(win, text="Générer tableau comparatif")
    button_generate.pack()
    button_add_date = tk.Button(win, text="Ajouter ou modifier des données")
    button_add_date.pack()
    button_view_data = tk.Button(win, text="Voir des données")
    button_view_data.pack()

    frame = tk.Frame(win)
    frame.pack(fill='both', expand=True)

    tree = ttk.Treeview(frame, columns=(1, 2, 3), show="headings", height=8)
    tree.pack(side='left', fill='both', expand=True)

    tree.heading(1, text="NomLieux")
    tree.heading(2, text="Description")
    tree.heading(3, text="Ville")

    for row in rows:
        tree.insert('', 'end', values=row)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')

    tree.configure(yscroll=scrollbar.set)

    ConDB.close()

def visitor():
    win_visitor = tk.Toplevel(root)
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

root = tk.Tk()
root.title("Analyse temps de parcours")
root.geometry("600x600")

title = tk.Label(root, text="Analyse de temps de parcours", font=("Arial", 25))
title.pack()

login = tk.Label(root, text="Entrez votre identifiant")
login.pack()

login_name = tk.StringVar()
name_entry = tk.Entry(root, textvariable=login_name)
name_entry.focus_set()
name_entry.pack()

password_label = tk.Label(root, text="Entrez votre mot de passe")
password_label.pack()

password_log = tk.StringVar()
password_entry = tk.Entry(root, textvariable=password_log, show="*")
password_entry.pack()

button_connect = tk.Button(root, text="Connexion", width=30, height=3, command=lambda: confirm_user(login_name.get(), password_log.get()))
button_connect.pack()

button_visitor = tk.Button(root, text="Se connecter en tant que visiteur", width=30, height=3, command=visitor)
button_visitor.pack()

root.mainloop()
