import pandas as pd

data = pd.read_csv('date.csv')

pd.wide_to_long('data.csv')