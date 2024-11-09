import pandas as pd

def confirm_user(name):
    user_list = pd.read_excel('liste_graphiqueur.xlsx')

    valid = 0

    print(user_list)

    for i in range (len(user_list)):
        if user_list['nom'][i] == name:
            valid = 1

    return (valid)