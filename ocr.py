import pytesseract
from PIL import Image
import pandas as pd

image = Image.open("Sans titre.png")
text = pytesseract.image_to_string(image)

#print(text)

lines = text.strip().split("\n")

premierPL = lines[14].strip().split()
print(premierPL)

for line in lines:
    ligne_separee = line.strip().split()
    print(ligne_separee)
