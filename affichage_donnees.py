import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
#from genere_tableau import export_tableau

columns = ["Arret d'origine", "Arret de fin", "Distance", "0:00", "7:00", "9:00", "15:30", "17:30"]

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

    item = tableau.item(cellule_select)
    valeurs = item["values"]

    # Identifier la colonne sélectionnée
    colonne = tableau.identify_column(event.x)
    colonne_index = int(colonne.replace("#", "")) - 1
    colonne_nom = columns[colonne_index]  # Utilisation des colonnes définies

    # Empêcher la modification des colonnes non éditables
    if colonne_nom in ["Arret d'origine", "Arret de fin", "Distance"]:
        messagebox.showinfo("Modification impossible", "Vous ne pouvez pas modifier cette colonne.")
        return

    ancienne_valeur = valeurs[colonne_index]
    nouvelle_valeur = simpledialog.askstring("Modifier", f"Modifier la valeur (actuelle : {ancienne_valeur})")

    if nouvelle_valeur is None or nouvelle_valeur.strip() == "":
        return

    try:
        connect = sqlite3.connect("listelieux.db")
        cursor = connect.cursor()

        # Récupération des données nécessaires pour identifier la paire de lieux
        lieu_depart = valeurs[0]  # Colonne "Arret d'origine"
        lieu_arrivee = valeurs[1]  # Colonne "Arret de fin"
        heure_debut = colonne_nom
        version = entry_version.get()

        # Vérifier l'existence de la paire de lieux et son identifiant unique
        requete_verification = """
        SELECT IDPaireLieux
        FROM PaireLieux
        WHERE LieuxDepart = ? AND LieuxArrivee = ?
        """
        cursor.execute(requete_verification, (lieu_depart, lieu_arrivee))
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Erreur", "La paire de lieux spécifiée n'existe pas.")
            return

        id_paire_lieux = result[0]

        # Mettre à jour le temps dans la base de données
        requete_update = """
        UPDATE TempsEntreLieux2
        SET Temps = ?
        WHERE PaireLieux = ? AND HeureDebut = ? AND VersionTemps = ?
        """
        cursor.execute(requete_update, (nouvelle_valeur, id_paire_lieux, heure_debut, version))
        connect.commit()

        if cursor.rowcount > 0:  # Vérifie si une ligne a été modifiée
            # Mettre à jour la valeur dans le tableau
            valeurs[colonne_index] = nouvelle_valeur
            tableau.item(cellule_select, values=valeurs)
            messagebox.showinfo("Succès", "Valeur mise à jour avec succès.")
        else:
            messagebox.showwarning("Avertissement", "Aucune modification n'a été effectuée.")

        # Vérifier les autres lignes qui utilisent cette paire de lieux
        requete_verification_lignes = """
        SELECT l.NumLigne, l.Sens
        FROM composition AS c
        JOIN Ligne AS l ON c.IdLigne = l.IDLigne
        WHERE c.IdPaireLieux = ?
        """
        cursor.execute(requete_verification_lignes, (id_paire_lieux,))
        lignes_associees = cursor.fetchall()

        if lignes_associees:
            lignes_message = "\n".join([f"Ligne {ligne[0]} (Sens {ligne[1]})" for ligne in lignes_associees])
            messagebox.showinfo(
                "Lignes associées",
                f"La paire de lieux modifiée est également utilisée par les lignes suivantes :\n{lignes_message}"
            )
        else:
            messagebox.showinfo("Aucune ligne associée", "Cette paire de lieux n'est utilisée par aucune autre ligne.")

    except sqlite3.Error as e:
        messagebox.showerror("Erreur SQL", f"Une erreur est survenue lors de la mise à jour : {e}")

    finally:
        if connect:
            connect.close()

def creer_nouvelle_version(version_source, nouvelle_version):
    try:
        connect = sqlite3.connect("listelieux.db")
        cursor = connect.cursor()

        cursor.execute("SELECT 1 FROM TempsEntreLieux2 WHERE VersionTemps = ?", (nouvelle_version,))
        if cursor.fetchone():
            messagebox.showwarning("Version existante", "La version que vous essayez de créer existe déjà.")
            return

        cursor.execute("""
            INSERT INTO TempsEntreLieux2 (HeureDebut, HeureFin, Temps, VersionTemps, PaireLieux)
            SELECT HeureDebut, HeureFin, Temps, ?, PaireLieux
            FROM TempsEntreLieux2
            WHERE VersionTemps = ?
        """, (nouvelle_version, version_source))

        connect.commit()
        messagebox.showinfo("Succès", f"La nouvelle version '{nouvelle_version}' a été créée avec succès !")

    except sqlite3.Error as e:
        messagebox.showerror("Erreur SQL", f"Une erreur est survenue lors de la création de la nouvelle version : {e}")

    finally:
        if connect:
            connect.close()

def affichage_DB(graphiqueur):
    global tableau, entry_version
    AnalyseDonnes = tk.Tk()
    AnalyseDonnes.title("Gestion des données")

    tableau = ttk.Treeview(AnalyseDonnes, columns=columns, show="headings", height=25)

    for col in columns:
        tableau.heading(col, text=col)
        tableau.column(col, width=150, anchor="center")
    if graphiqueur:
        tableau.bind("<Double-1>", update_cellule)

    tableau.pack(fill="both", expand=True)

    frame = tk.Frame(AnalyseDonnes, pady=10)
    frame.pack()

    label_version = tk.Label(frame, text="Version :")
    label_version.grid(row=0, column=0, padx=5)
    entry_version = tk.Entry(frame, width=10)
    entry_version.grid(row=0, column=1, padx=5)

    label_ligne = tk.Label(frame, text="Ligne :")
    label_ligne.grid(row=0, column=2, padx=5)
    entry_ligne = tk.Entry(frame, width=10)
    entry_ligne.grid(row=0, column=3, padx=5)

    label_sens = tk.Label(frame, text="Sens :")
    label_sens.grid(row=0, column=4, padx=5)
    entry_sens = tk.Entry(frame, width=10)
    entry_sens.grid(row=0, column=5, padx=5)
    if graphiqueur:
        label_version_source = tk.Label(frame, text="Version source :")
        label_version_source.grid(row=1, column=0, padx=5)
        entry_version_source = tk.Entry(frame, width=10)
        entry_version_source.grid(row=1, column=1, padx=5)

        label_nouvelle_version = tk.Label(frame, text="Nouvelle version :")
        label_nouvelle_version.grid(row=1, column=2, padx=5)
        entry_nouvelle_version = tk.Entry(frame, width=10)
        entry_nouvelle_version.grid(row=1, column=3, padx=5)

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

    if graphiqueur:
        def on_creer_version():
            version_source = entry_version_source.get()
            nouvelle_version = entry_nouvelle_version.get()
            if not version_source or not nouvelle_version:
                messagebox.showwarning("Champs manquants", "Veuillez remplir les champs pour copier une version.")
                return
            creer_nouvelle_version(version_source, nouvelle_version)

        btn_creer_version = tk.Button(frame, text="Créer une nouvelle version", command=on_creer_version)
        btn_creer_version.grid(row=1, column=6, padx=10)

    #btn_export = tk.Button(frame, text="Exporter vers Excel", command=lambda: export_tableau(tableau, columns))
    #btn_export.grid(row=0, column=7, padx=10)

    AnalyseDonnes.mainloop()

#affichage_DB(True)