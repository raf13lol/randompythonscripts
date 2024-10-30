import os
from PIL import Image
from time import sleep

maxsize = 2048
PATH = os.path.dirname(__file__)

def workOnImage(index, imageList):
    image = Image.new("RGBA", (maxsize, maxsize))
    width = 0
    height = 0

    topLeftX = 0
    topLeftY = 0

    print(f"\n'texturepage{str(index)}.png' being created...")

    while len(imageList) > 0:
        toimport = imageList[0]
        tiw = toimport.size[0]
        tih = toimport.size[1]

        if not tih > tiw:
            if topLeftY + tih >= maxsize:
                topLeftX = width
                topLeftY = 0
        else:
            if topLeftX + tiw >= maxsize:
                topLeftY = height
                topLeftX = 0

        if topLeftX + tiw >= maxsize or topLeftY + tih >= maxsize:
            break
        else:
            imageList.remove(toimport)

        image.paste(toimport, (topLeftX, topLeftY))
        width = max(topLeftX + tiw, width)
        height = max(topLeftY + tih, height)
        if not tih > tiw:
            topLeftY += tih
        else:
            topLeftX += tiw

    if width + height > 0:
        print("Done! Just wait a moment...")
        sleep(0.25)
        image.save(f"{PATH}/texturepage{str(index)}.png")
        print(f"'texturepage{str(index)}.png' created!")

    if len(imageList) > 0:
        workOnImage(index + 1, imageList)

print("\nスタート！")

er = []
listdir = os.listdir(PATH + "/")
for asd in listdir:
    if asd.startswith("texturepage") or not asd.endswith(".png"):
        continue
    er.append(Image.open(PATH + "/" + asd))
er.sort(key=lambda i: i.size[0] * i.size[1], reverse=True)

print(str(len(er)) + " files detected!")

workOnImage(0, er)