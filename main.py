import tkinter as tk
from math import trunc
from tkinter import messagebox, ttk, LabelFrame
import sqlite3
from affichage_donnees import affichage_DB
from gestionDB import add_lieux, add_duo_lieux, add_temps_parcours, Creer_ligne, Composition_ligne
from objetdb import NomLieux
from genere_tableau import export_comparaison_excel

def graph_select(graphiqueur):
    graphiqueur = True

    ConDB = sqlite3.connect("listelieux.db")
    cursor = ConDB.cursor()

    cursor.execute("SELECT * FROM NomLieux")
    rows = cursor.fetchall()

    win = tk.Toplevel(root)
    win.title("Section")
    win.geometry("500x500")

    login_graph_select = tk.Label(win, textvariable=login_name)
    login_graph_select.pack()

    button_generate = tk.Button(win, text="gestion des lieux", width=30, height=3,
                               command=lambda: gestionLieux())
    button_generate.pack()

    button_ligne = tk.Button(win, text="gestion des lignes", width=30, height=3,
                                command=lambda: Creation_ligne())
    button_ligne.pack()

    button_analyse = tk.Button(win, text="Analyse des données", width=30, height=3,
                                command=lambda: affichage_DB(graphiqueur))
    button_analyse.pack()

    #frame = tk.Frame(win)
    #frame.pack(fill='both', expand=True)

    #tree = ttk.Treeview(frame, columns=(1, 2, 3), show="headings", height=8)
    #tree.pack(side='left', fill='both', expand=True)

    #tree.heading(1, text="NomLieux")
    #tree.heading(2, text="Description")
    #tree.heading(3, text="Ville")

    #for row in rows:
        #tree.insert('', 'end', values=row)

    #scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    #scrollbar.pack(side='right', fill='y')


    frame = tk.Frame(win, pady=10)
    frame.pack()

    label_versionactu = tk.Label(frame, text="Version actuelle :")
    label_versionactu.grid(row=0, column=0, padx=5)
    entry_versionactu = tk.Entry(frame, width=10)
    entry_versionactu.grid(row=0, column=1, padx=5)

    label_versionpropo = tk.Label(frame, text="Version proposition :")
    label_versionpropo.grid(row=0, column=2, padx=5)
    entry_versionpropo = tk.Entry(frame, width=10)
    entry_versionpropo.grid(row=0, column=3, padx=5)

    label_ligne = tk.Label(frame, text="Ligne :")
    label_ligne.grid(row=1, column=0, padx=5)
    entry_ligne = tk.Entry(frame, width=10)
    entry_ligne.grid(row=1, column=1, padx=5)

    label_sens = tk.Label(frame, text="Sens :")
    label_sens.grid(row=1, column=2, padx=5)
    entry_sens = tk.Entry(frame, width=10)
    entry_sens.grid(row=1, column=3, padx=5)

    versionactuel = entry_versionactu.get()
    versionpropo = entry_versionpropo.get()
    ligne = entry_ligne.get()
    sens = entry_sens.get()

    button_fichier_excel = tk.Button(win, text="générer fichier comparatif", width=30, height=3,
                                     command=lambda: export_comparaison_excel(entry_versionactu.get(),
                                                                              entry_versionpropo.get(),
                                                                              entry_ligne.get(),
                                                                              entry_sens.get(),
                                                                              "comparaison_lignes.xlsx"))

    button_fichier_excel.pack()

    ConDB.close()

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
        graph_select(graphiqueur)
        #print("Utilisateur:", utilisateur)
    else:
        messagebox.showerror("ERREUR", "Nom d'utilisateur ou mot de passe incorrect")

def gestionLieux():
    win_gestionLIeux = tk.Toplevel(root)
    win_gestionLIeux.title("gestion des lieux")
    win_gestionLIeux.geometry("600x800")

    GLieux = LabelFrame(win_gestionLIeux, text="gestion arrêts", padx=20, pady=2, height=200)
    GLieux.pack(fill="both", expand="yes")

    login = tk.Label(GLieux, text="Entrez le nom d'un Lieux")
    login.pack()

    IDLieux = tk.StringVar()
    name_entry = tk.Entry(GLieux, textvariable=IDLieux)
    #name_entry.focus_set()
    name_entry.pack()

    login = tk.Label(GLieux, text="Entrez la description du lieux")
    login.pack()

    Description = tk.StringVar()
    name_entry = tk.Entry(GLieux, textvariable=Description)
    #name_entry.focus_set()
    name_entry.pack()

    login = tk.Label(GLieux, text="Entrez le nom de la ville")
    login.pack()

    Ville = tk.StringVar()
    name_entry = tk.Entry(GLieux, textvariable=Ville)
    #name_entry.focus_set()
    name_entry.pack()

    button_connect = tk.Button(GLieux, text="création de Lieux", width=30, height=3,
                               command=lambda: add_lieux(IDLieux.get(), Description.get(), Ville.get()))

    button_connect.pack()

    GPLieux = LabelFrame(win_gestionLIeux, text="gestion les paires d'arrêts", padx=20, pady=2, height=200)
    GPLieux.pack(fill="both", expand="yes")

    gestionPL = tk.Label(GPLieux, text="création paire de lieux")
    gestionPL.pack()

    lieuxdebut_objets = NomLieux.item_db(NomLieux)
    lieux_nomsDebut = [lieu.nom_lieux for lieu in lieuxdebut_objets]

    listelieuxDebut = ttk.Combobox(GPLieux, values=lieux_nomsDebut)
    listelieuxDebut.pack()

    lieuxfin_objets = NomLieux.item_db(NomLieux)
    lieux_nomsFin = [lieu.nom_lieux for lieu in lieuxfin_objets]

    listelieuxFin = ttk.Combobox(GPLieux, values=lieux_nomsFin)
    listelieuxFin.pack()

    gestionPL = tk.Label(GPLieux, text="Ajoutez la distance entre ces lieux (en mètre)")
    gestionPL.pack()
    distancePL = tk.StringVar()
    distance_entry = tk.Entry(GPLieux, textvariable=distancePL)
    distance_entry.pack()

    button_ajoutPL = tk.Button(GPLieux, text="création de la paire de lieux", width=30, height=3,
                               command=lambda: add_duo_lieux(listelieuxDebut.get(), listelieuxFin.get(), int(distancePL.get())))
    button_ajoutPL.pack()

    GTempsParcours = LabelFrame(win_gestionLIeux, text="gestion des temps de parcours", padx=20, pady=2, height=200)
    GTempsParcours.pack(fill="both", expand="yes")

    gestionTPL = tk.Label(GTempsParcours, text="choisissez un lieux de bébut et un lieux de fin")
    gestionTPL.pack()

    lieuxdebut_objets = NomLieux.item_db(NomLieux)
    lieux_nomsDebut = [lieu.nom_lieux for lieu in lieuxdebut_objets]

    TlistelieuxDebut = ttk.Combobox(GTempsParcours, values=lieux_nomsDebut)
    TlistelieuxDebut.pack()

    lieuxfin_objets = NomLieux.item_db(NomLieux)
    lieux_nomsFin = [lieu.nom_lieux for lieu in lieuxfin_objets]

    TlistelieuxFin = ttk.Combobox(GTempsParcours, values=lieux_nomsFin)
    TlistelieuxFin.pack()

    gestionTPL = tk.Label(GTempsParcours, text="choisissez un lieux de bébut et un lieux de fin")
    gestionTPL.pack()

    HDebut = tk.StringVar()
    name_entry = tk.Entry(GTempsParcours, textvariable=HDebut)
    name_entry.pack()

    HFin = tk.StringVar()
    name_entry = tk.Entry(GTempsParcours, textvariable=HFin)
    name_entry.pack()

    gestionTPL = tk.Label(GTempsParcours, text="choisissez un lieux de bébut et un lieux de fin au format XX:XX")
    gestionTPL.pack()


    gestionTPL = tk.Label(GTempsParcours, text="mettez le temps de parcours")
    gestionTPL.pack()

    TempsP = tk.StringVar()
    name_entry = tk.Entry(GTempsParcours, textvariable=TempsP)
    name_entry.pack()

    gestionTPL = tk.Label(GTempsParcours, text="mettez la version de temps de parcours")
    gestionTPL.pack()

    VTempsP = tk.StringVar()
    name_entry = tk.Entry(GTempsParcours, textvariable=VTempsP)
    name_entry.pack()

    button_ajoutTP = tk.Button(GTempsParcours, text="Ajout Temps de parcours", width=30, height=3,
                               command=lambda: add_temps_parcours(HDebut.get(), HFin.get(),
                                                             int(TempsP.get()), VTempsP.get(), TlistelieuxDebut.get(),TlistelieuxFin.get()))
    button_ajoutTP.pack()

def Creation_ligne():

    win_ligne = tk.Toplevel(root)
    win_ligne.title("création de ligne")
    win_ligne.geometry("800x900")

    GLigne = LabelFrame(win_ligne, text="gestion des temps de parcours", padx=20, pady=2, height=200)
    GLigne.pack(fill="both", expand="yes")

    Crealigne = tk.Label(GLigne, text="Création d'une ligne")
    Crealigne.pack()

    lignenumb = tk.Label(GLigne, text="entrez le numéro de la ligne")
    lignenumb.pack()

    NumLigne = tk.StringVar()
    NumeroLigne = tk.Entry(GLigne, textvariable=NumLigne)
    NumeroLigne.pack()

    sensligne = tk.Label(GLigne, text="mettez le sens de la ligne")
    sensligne.pack()

    SensLigne = tk.StringVar()
    Sens = tk.Entry(GLigne, textvariable=SensLigne)
    Sens.pack()

    button_ajoutligne = tk.Button(GLigne, text="création de la ligne", width=30, height=3,
                               command=lambda: Creer_ligne(int(NumLigne.get()), int(SensLigne.get())))
    button_ajoutligne.pack()

    AjoutPL = LabelFrame(win_ligne, text="gestion les paires d'arrêts", padx=20, pady=2, height=200)
    AjoutPL.pack(fill="both", expand="yes")

    CompLigne = tk.Label(AjoutPL, text="entrez le numéro de la ligne")
    CompLigne.pack()

    CompostionL = tk.StringVar()
    NumeroLigne = tk.Entry(AjoutPL, textvariable=CompostionL)
    NumeroLigne.pack()

    ComSens = tk.Label(AjoutPL, text="mettez le sens de la ligne")
    ComSens.pack()

    CompostionS = tk.StringVar()
    Sens = tk.Entry(AjoutPL, textvariable=CompostionS)
    Sens.pack()

    gestionPL = tk.Label(AjoutPL, text="création paire de lieux")
    gestionPL.pack()

    lieuxdebut_objets = NomLieux.item_db(NomLieux)
    lieux_nomsDebut = [lieu.nom_lieux for lieu in lieuxdebut_objets]

    listelieuxDebut = ttk.Combobox(AjoutPL, values=lieux_nomsDebut)
    listelieuxDebut.pack()

    lieuxfin_objets = NomLieux.item_db(NomLieux)
    lieux_nomsFin = [lieu.nom_lieux for lieu in lieuxfin_objets]

    listelieuxFin = ttk.Combobox(AjoutPL, values=lieux_nomsFin)
    listelieuxFin.pack()

    button_ajoutPLaLigne = tk.Button(AjoutPL, text="ajout paire de lieux à une ligne", width=30, height=3,
                                  command=lambda: Composition_ligne(int(CompostionL.get()), int(CompostionS.get()) ,listelieuxDebut.get(), listelieuxFin.get()))
    button_ajoutPLaLigne.pack()

    #AjoutPL.mainloop()

def Analyse_donnée():

    win_analyse = tk.Toplevel(root)
    win_analyse.title("Analyse des données")
    win_analyse.geometry("800x900")

    label = tk.Label(win_analyse, text="ça commence ici")
    label.pack()

    #win_analyse.mainloop()

def visitor(graphiqueur):
    win_visitor = tk.Toplevel(root)
    win_visitor.title("Voir des données")

root = tk.Tk()
root.title("Analyse temps de parcours")
root.geometry("600x600")

graphiqueur = None

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

button_visitor = tk.Button(root, text="Se connecter en tant que visiteur", width=30, height=3, command=lambda :affichage_DB(graphiqueur))
button_visitor.pack()

root.mainloop()
