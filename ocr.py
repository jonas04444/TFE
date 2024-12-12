import pytesseract
from PIL import Image

# Charger une image pour tester
image = Image.open("Sans titre.png")  # Remplacez par le chemin de votre image
text = pytesseract.image_to_string(image)
print("Texte extrait :", text)

