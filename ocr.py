import pytesseract
from PIL import Image
import pandas as pd

image = Image.open("Sans titre.png")
text = pytesseract.image_to_string(image)

lines = text.strip().split("\n")
firstline = -1
lastline = -1

for i,index in enumerate(lines):
    if "Orig." in index:
        firstline = i
    elif "Total" in index:
        lastline = i
        break

tranchehoraire = lines[firstline-1].split()
for i in range (len(tranchehoraire)):
    print(tranchehoraire[i])

for i in lines [firstline-1:lastline+1]:
    print(i.strip().split())
