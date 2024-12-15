import pytesseract
from PIL import Image
import pandas as pd

image = Image.open("Sans titre.png")
text = pytesseract.image_to_string(image)

#print(text)

lines = text.strip().split("\n")
firstline = -1
lastline = -1

for i,index in enumerate(lines):
    if "Orig." in index:
        firstline = i
    elif "Total" in index:
        lastline = i
        break

#premierPL = lines[firstline-1].strip().split()
#print(premierPL)

for i in lines [firstline-1:lastline+1]:
    print(i.strip().split())
#for line in lines:
#    ligne_separee = line.strip().split()
#    print(ligne_separee)
