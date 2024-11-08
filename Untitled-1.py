from tkinter import *

def graph_select():
    win = Toplevel(root)
    win.title("selection")
    win.geometry("500x500")

root = Tk()

root.title("analyse temps de parcours")
root.geometry("600x600")
root.iconbitmap("logo-tec.ico")

title = Label(root, text="analyse de temps de parcours", font=("Arial", 25))
title.pack()

button_connect = Button(root, text="connexion", command = graph_select)
button_connect.pack()

root.mainloop()