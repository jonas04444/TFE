import pytesseract
from PIL import Image
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog
import cv2
from pytesseract import image_to_string
from gestionDB import add_duo_lieux

def OCR():
    #qgrid pour éditer tableau
    chemin_fichier = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    image= cv2.imread(chemin_fichier)
    #image = Image.open("Sans titre.png")
    text = pytesseract.image_to_string(image)

    lines = text.strip().split("\n")
    firstline = -1
    lastline = -1

    for i, index in enumerate(lines):
        if "Orig." in index:
            firstline = i
        elif "Total" in index:
            lastline = i
            break

    for line in lines:
        print(line.strip().split())
    if firstline == -1 or lastline == -1:
        raise ValueError("Impossible de trouver les sections 'Orig.' ou 'Total' dans les données.")

    if firstline > 0:
        tranchehoraire = lines[firstline - 1].split()
    else:
        tranchehoraire = []

    data = [line.strip().split() for line in lines[firstline + 1:lastline]]

    cleaned_data = [[value for value in row if value != "="] for row in data]

    for i, row in enumerate(cleaned_data):
        if len(row) != len(cleaned_data[0]):
            print(f"trop de colonne")

    columns = ["Orig.", "Dest.", "Dist."] + tranchehoraire

    max_len = len(columns)
    normalized_data = [row + [""] * (max_len - len(row)) if len(row) < max_len else row[:max_len] for row in cleaned_data]

    df = pd.DataFrame(normalized_data, columns=columns)

    for col in df.columns[2:]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    total_row = ["Total", ""] + [df[col].sum() for col in df.columns[2:]]
    df.loc[len(df)] = total_row

    root = tk.Tk()
    root.title("Test Tableau")
    root.geometry("900x600")

    table_frame = tk.Frame(root)
    table_frame.pack(fill="both", expand=True)

    tableauhoraire = ttk.Treeview(table_frame, columns=list(df.columns), show="headings", height=20)

    for col in df.columns:
        tableauhoraire.heading(col, text=col)
        tableauhoraire.column(col, width=100, anchor="center")

    for _, row in df.iterrows():
        tableauhoraire.insert("", tk.END, values=list(row))

    tableauhoraire.pack(fill="both", expand=True)

    button_import = tk.Button(table_frame, text="inporter paire lieux", width=30, height=3,
                               command=lambda: validation(firstline, lastline, lines))
    button_import.pack()

    root.mainloop()
def validation(firstline, lastline, lines):
    for line in lines[firstline + 1:lastline]:
        Start = (line.strip().split()[0])
        End = (line.strip().split()[1])
        Distance = (line.strip().split()[2])
        print(line.strip().split()[:3])
        add_duo_lieux(Start,End,Distance)



#OCR()