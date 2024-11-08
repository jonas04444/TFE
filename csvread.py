import pandas as pd

def confirm_user(name):
    user_list = pd.read_excel('liste_graphiqueur.xlsx')

    print(user_list)

    for i in range (len(user_list)):
        print(user_list['nom'][i])
        if user_list['nom'][i] == name:
            print("c'est bon")

name = "kellner"
confirm_user(name)