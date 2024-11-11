from tkinter import *
from gestionDB import add_user, confirm_user


def graph_select():
    win = Toplevel(root)
    win.title("section")
    login_graph_select = Label(win, textvariable=login_name)
    login_graph_select.pack()
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

login = Label(root, text="entrez votre identifiant")
login.pack()

login_name = StringVar()
name = Entry(root, textvariable=login_name)
name.focus_set()
name.pack()

password = Label(root, text="entrez votre mot de passe")
password.pack()

password_log = StringVar()
password_log = Entry(root, textvariable=password_log)
password_log.focus_set()
password_log.pack()

button_connect = Button(root, text="connexion", width=30 , height=3, command=lambda: confirm_user(login_name.get(), password_log.get()))
button_connect.pack()

button_visitor = Button(root, text="se connecter en tant que visiteur",width=30 , height=3, command=visitor)
button_visitor.pack()

root.mainloop()