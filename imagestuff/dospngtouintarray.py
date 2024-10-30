from PIL import Image
import math,os

PATH = os.path.dirname(__file__) + "/"

def doimage(path):
    p = path
    img = Image.open(p)
    img = img.convert("RGBA")

    pixdata = img.load()
    PIXELDATATOSAVEASCARRAYFUCK = []

    for y in range(math.floor(img.size[1]/16)):
        for x in range(math.floor(img.size[0]/8)):
            PixelData1 = int(0)
            PixelData2 = int(0)
            PixelData3 = int(0)
            PixelData4 = int(0)

            for bit in range(128):
                orvalue = 0
                if pixdata[x*8+(bit % 8), y * 16 + math.floor(bit / 8)] == (255, 255, 255, 255):
                    orvalue = 1 << (bit % 32)
                match (math.floor(bit / 32)):
                    case 0:
                        PixelData1 |= orvalue
                    case 1:
                        PixelData2 |= orvalue
                    case 2:
                        PixelData3 |= orvalue
                    case 3:
                        PixelData4 |= orvalue
                        
            PIXELDATATOSAVEASCARRAYFUCK.append(PixelData1)
            PIXELDATATOSAVEASCARRAYFUCK.append(PixelData2)
            PIXELDATATOSAVEASCARRAYFUCK.append(PixelData3)
            PIXELDATATOSAVEASCARRAYFUCK.append(PixelData4)
    file = open(PATH + "dosCodePage.glsl_array", "x")
    file.write(dataIntoC_Array(PIXELDATATOSAVEASCARRAYFUCK))
    file.close()

def dataIntoC_Array(data):
    space = "    "
    strs = f'uint dosCodePageFont[{4 * 256}] = uint[](' 
    for i in range(len(data)):
        if i % 4 == 0:
            strs += f"\n{space}"
            strs += f"\n{space}// character code {math.floor(i/4)}"
            if i != 0:
                strs += f"\n{space}"
            else:
                strs += f"\n{space}"
        hexstr = str(data[i]) + "u"
        strs += hexstr
        if i != len(data)-1:
            strs += ", "
    strs += "\n);"
    return strs

doimage(PATH + "dos.png")