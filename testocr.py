import pytesseract
from PIL import Image
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox


def load_image_and_process():
    # Charger l'image et extraire le texte avec OCR
    image_path = filedialog.askopenfilename(title="Sélectionnez une image", filetypes=[("Images", "*.png *.jpg *.jpeg")])
    if not image_path:
        return

    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)

    # Découper le texte par lignes
    lines = text.strip().split("\n")

    # Traiter les données extraites
    data_rows = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 3:
            try:
                float(parts[2])  # Vérifier que la troisième colonne est un nombre
                data_rows.append(parts)
            except ValueError:
                continue

    if not data_rows:
        messagebox.showerror("Erreur", "Aucune donnée valide extraite de l'image.")
        return

    # Construire les colonnes
    max_cols = max(len(row) for row in data_rows)
    columns = ["Orig.", "Dest.", "Dist."] + [f"Time {i+1}" for i in range(max_cols - 3)]

    # Créer un DataFrame pour simplifier la gestion des données
    global df
    df = pd.DataFrame(data_rows, columns=columns[:max_cols])

    # Afficher les données dans l'interface
    display_table()


def display_table():
    # Réinitialiser le tableau Treeview
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Création du tableau Treeview
    tree = ttk.Treeview(table_frame, columns=list(df.columns), show="headings", height=20)

    # Définir les colonnes
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # Insérer les données dans le tableau
    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

    tree.pack(fill="both", expand=True)

    # Ajouter un bouton pour sauvegarder les modifications
    save_button = tk.Button(table_frame, text="Sauvegarder en CSV", command=save_to_csv)
    save_button.pack(pady=10)


def save_to_csv():
    # Enregistrer le tableau modifié dans un fichier CSV
    save_path = filedialog.asksaveasfilename(title="Enregistrer sous", defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")])
    if save_path:
        df.to_csv(save_path, index=False)
        messagebox.showinfo("Succès", f"Tableau sauvegardé sous {save_path}")


# Création de l'interface Tkinter
root = tk.Tk()
root.title("OCR Tableau Modifiable")
root.geometry("900x600")

# Ajouter un bouton pour charger une image
load_button = tk.Button(root, text="Charger une image", command=load_image_and_process)
load_button.pack(pady=10)

# Cadre pour afficher le tableau
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True)

# Lancer l'application
root.mainloop()
