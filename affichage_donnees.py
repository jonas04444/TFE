import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def afficher_donnees(version, numero_ligne, sens):
    try:
        connect = sqlite3.connect("listelieux.db")
        cursor = connect.cursor()

        requeteSQL = """
        SELECT 
            pl.LieuxDepart AS "Arrêt d'origine", 
            pl.LieuxArrivee AS "Arrêt de fin", 
            pl.Distance AS "Distance", 
            COALESCE(tl0.Temps, '') AS "0:00", 
            COALESCE(tl7.Temps, '') AS "7:00", 
            COALESCE(tl9.Temps, '') AS "9:00", 
            COALESCE(tl15.Temps, '') AS "15:30", 
            COALESCE(tl17.Temps, '') AS "17:30"
        FROM PaireLieux AS pl
        LEFT JOIN TempsEntreLieux2 AS tl0 ON pl.IDPaireLieux = tl0.PaireLieux AND tl0.HeureDebut = '0:00' AND tl0.VersionTemps = ?
        LEFT JOIN TempsEntreLieux2 AS tl7 ON pl.IDPaireLieux = tl7.PaireLieux AND tl7.HeureDebut = '7:00' AND tl7.VersionTemps = ?
        LEFT JOIN TempsEntreLieux2 AS tl9 ON pl.IDPaireLieux = tl9.PaireLieux AND tl9.HeureDebut = '9:00' AND tl9.VersionTemps = ?
        LEFT JOIN TempsEntreLieux2 AS tl15 ON pl.IDPaireLieux = tl15.PaireLieux AND tl15.HeureDebut = '15:30' AND tl15.VersionTemps = ?
        LEFT JOIN TempsEntreLieux2 AS tl17 ON pl.IDPaireLieux = tl17.PaireLieux AND tl17.HeureDebut = '17:30' AND tl17.VersionTemps = ?
        WHERE pl.IDPaireLieux IN (
            SELECT c.IdPaireLieux 
            FROM composition AS c
            JOIN Ligne AS l ON c.IdLigne = l.IDLigne
            WHERE l.NumLigne = ? AND l.Sens = ?
        )
        ORDER BY pl.IDPaireLieux;
        """

        cursor.execute(requeteSQL, (version, version, version, version, version, numero_ligne, sens))
        datas = cursor.fetchall()

        tableau.delete(*tableau.get_children())
        for data in datas:
            tableau.insert("", tk.END, values=data)

    except sqlite3.Error as e:
        messagebox.showerror("ERREUR SQL", f"lecture données impossible : {e}")

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
tableau = ttk.Treeview(AnalyseDonnes, columns=columns, show="headings", height=25)

for col in columns:
    tableau.heading(col, text=col)
    tableau.column(col, width=150, anchor="center")

frame = tk.Frame(AnalyseDonnes, pady=10)
frame.pack()

label_version = tk.Label(frame, text="Version:")
label_version.grid(row=0, column=0, padx=5)
entry_version = tk.Entry(frame, width=10)
entry_version.grid(row=0, column=1, padx=5)

label_ligne = tk.Label(frame, text="Ligne:")
label_ligne.grid(row=0, column=2, padx=5)
entry_ligne = tk.Entry(frame, width=10)
entry_ligne.grid(row=0, column=3, padx=5)

label_sens = tk.Label(frame, text="Sens:")
label_sens.grid(row=0, column=4, padx=5)
entry_sens = tk.Entry(frame, width=10)
entry_sens.grid(row=0, column=5, padx=5)

def on_afficher():
    version = entry_version.get()
    numero_ligne = entry_ligne.get()
    sens = entry_sens.get()
    if not version or not numero_ligne or not sens:
        messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs avant de continuer.")
        return
    afficher_donnees(version, numero_ligne, sens)

btn_afficher = tk.Button(frame, text="Afficher", command=on_afficher)
btn_afficher.grid(row=0, column=6, padx=10)

tableau.pack(fill="both", expand=True)
AnalyseDonnes.mainloop()
