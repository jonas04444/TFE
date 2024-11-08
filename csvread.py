import pandas as pd

user_list = pd.read_excel('liste_graphiqueur.xlsx')

print(user_list)

for i in range (len(user_list)):
    print(user_list['nom'][i])