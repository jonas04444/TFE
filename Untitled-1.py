from tkinter import *

def graph_select():
    win = Toplevel(root)
    win.title("selection")
    win.geometry("500x500")
    button_generate = Button(win, text="générer tableau comparatif")
    button_generate.pack()
    button_add_date = Button(win, text="ajouter ou modifier des données")
    button_add_date.pack()
    button_view_data = Button(win, text="voir des données")
    button_view_data.pack()

def visitor():
    win_visitor = Toplevel(root)
    win_visitor.title("voir des données")

root = Tk()

root.title("analyse temps de parcours")
root.geometry("600x600")
root.iconbitmap("logo-tec.ico")

title = Label(root, text="analyse de temps de parcours", font=("Arial", 25))
title.pack()

button_connect = Button(root, text="connexion", command = graph_select)
button_connect.pack()
button_visitor = Button(root, text="se connecter en tant que visiteur", command=visitor)
button_visitor.pack()

root.mainloop()