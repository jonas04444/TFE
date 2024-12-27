import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def afficher_donnees():
    try:
        connect = sqlite3.connect("listelieux.db")
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM PaireLieux")
        datas = cursor.fetchall()

        for data in datas:
            tableau.insert("", tk.END, values = data)
        print(tableau)

    except sqlite3.Error:
        messagebox.showerror("ERREUR SQL", "lecture données impossible")

    finally:
        if connect:
            connect.close()

def update_cellule(event):
    cellule_select = tableau.focus()
    if not cellule_select:
        return

    columns_id = tableau.identify_column(event.x)
    columns_index = int(columns_id.replace("#", "")) - 1
    valeur_cellule = tableau.item(cellule_select, "values")
    valeur_base = valeur_cellule[columns_index]

    nouvelle_valeur = simpledialog.askstring("modifier", f"Modifier la valeur : (actuelle : {valeur_base})")
    if nouvelle_valeur is None:
        return

AnalyseDonnes = tk.Tk()
AnalyseDonnes.title("affichage des données")

columns = ["Arret d'origine", "Arret de fin", "distance" ,"0:00", "7:00", "9:00", "15:30", " 17:30"]
tableau = ttk.Treeview(AnalyseDonnes, columns= columns, show="headings", height=20)

for col in columns:
    tableau.heading(col, text=col)
    tableau.column(col, width=150, anchor="center")

tableau.pack()

AnalyseDonnes.mainloop()