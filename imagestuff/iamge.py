# https://stackoverflow.com/questions/3752476/python-pil-replace-a-single-rgba-color
from PIL import Image
import math,os

PATH = os.path.dirname(__file__) + "/"

def doimage(path):
    p = path
    img = Image.open(p)
    img = img.convert("RGBA")

    pixdata = img.load()
    PIXELDATATOSAVEASCARRAYFUCK = []

    for y in range(img.size[1]):
        for x in range(math.floor(img.size[0]/8)):
            Pixel = 0
            for bit in range(8):
                if pixdata[x*8+bit, y] == (255, 255, 255, 255):
                    Pixel |= 1 << bit
            PIXELDATATOSAVEASCARRAYFUCK.append(Pixel)
    file = open(PATH + "image.c_array", "x")
    file.write(dataIntoC_Array(PIXELDATATOSAVEASCARRAYFUCK))
    file.close()
    
def dataIntoC_Array(data):
    space = "    "
    str = "const unsigned char bImage [] PROGMEM = {" 
    # 16 bytes per row
    for i in range(len(data)):
        if i % 16 == 0:
            str += f"\n{space}"
        hexstr = hex(data[i])
        if len(hexstr) == 3:
            hexstr = "0x0" + hexstr[2]
        str += hexstr
        if i != len(data)-1:
            str += ", "
    str += "\n};"
    return str


doimage(PATH + "image.png")

print("Donezing!")