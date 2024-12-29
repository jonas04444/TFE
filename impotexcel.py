import sqlite3
import pandas as pd
from gestionDB import add_lieux, add_duo_lieux, add_temps_parcours


def add_lieux_unique(IDLieux, Description, Ville):

    try:
        connect = sqlite3.connect("listelieux.db")
        cursor = connect.cursor()
        cursor.execute("SELECT COUNT(*) FROM NomLieux WHERE NomLieux = ?", (IDLieux,))
        exists = cursor.fetchone()[0]

        if exists == 0:
            add_lieux(IDLieux, Description, Ville)
    except sqlite3.Error as e:
        print(f"Erreur lors de la vérification ou de l'ajout du lieu : {e}")
    finally:
        if connect:
            connect.close()


def import_excel_to_db(filepath):
    try:
        df = pd.read_excel(filepath)

        df.columns = [col.strip() for col in df.columns]

        required_columns = ['Orig.', 'Dest.', 'Dist.', '0:00', '7:00', '9:00', '15:30', '17:30']
        print("Colonnes détectées :", df.columns.tolist())
        if not all(col in df.columns for col in required_columns):
            raise ValueError(
                f"Colonnes manquantes. Colonnes requises : {required_columns}. Colonnes trouvées : {df.columns.tolist()}")

        for index, row in df.iterrows():

            lieux_depart = row['Orig.']
            lieux_arrivee = row['Dest.']
            distance = float(row['Dist.'])
            temps_0 = row['0:00']
            temps_7 = row['7:00']
            temps_9 = row['9:00']
            temps_15 = row['15:30']
            temps_17 = row['17:30']

            add_lieux_unique(lieux_depart, f"Description de {lieux_depart}", "Ville")
            add_lieux_unique(lieux_arrivee, f"Description de {lieux_arrivee}", "Ville")

            add_duo_lieux(lieux_depart, lieux_arrivee, distance)

            if pd.notna(temps_0):
                add_temps_parcours("0:00", "6:59", int(temps_0), "202502", lieux_depart, lieux_arrivee)
            if pd.notna(temps_7):
                add_temps_parcours("7:00", "8:59", int(temps_7), "202502", lieux_depart, lieux_arrivee)
            if pd.notna(temps_9):
                add_temps_parcours("9:00", "15:29", int(temps_9), "202502", lieux_depart, lieux_arrivee)
            if pd.notna(temps_15):
                add_temps_parcours("15:30", "17:29", int(temps_15), "202502", lieux_depart, lieux_arrivee)
            if pd.notna(temps_17):
                add_temps_parcours("17:30", "32:00", int(temps_17), "202502", lieux_depart, lieux_arrivee)

        print("Données importées avec succès dans la base de données.")
    except Exception as e:
        print(f"Erreur lors de l'importation des données : {e}")

import_excel_to_db("63aller.xlsx")
