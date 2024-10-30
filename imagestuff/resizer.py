from PIL import Image
import os

PATH = input("dir? ") + "/"

def doimage(path):
    p = path
    img = Image.open(p)
    img = img.resize((img.size[0] * 2, img.size[1] * 2), Image.Resampling.NEAREST)
    img.save(p)

for image in os.listdir(PATH):
    if image.endswith(".png"):
        doimage(PATH + image)

print("Donezing!")