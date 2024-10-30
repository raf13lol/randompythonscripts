from PIL import Image
import sys, math, os

PATH = os.path.dirname(__file__)

textDictorany = [" ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
colors = [(0, 0, 0, 255), (255, 255, 255, 255), (255, 0, 255, 255)]

option = input("do you want to cipher or decipher a string? ('c' or 'd') ")
while option != 'c' and option != 'd':
    print("Invalid option")
    option = input("do you want to cipher or decipher a string? ('c' or 'd') ")

if option == "c":
    text = input("text to cipher (must be A-Z and spaces only, nothing else) ").upper()

    letterNumbers = []

    lettersFine = True
    for letter in text:
        try:
            letterNumbers.append(textDictorany.index(letter))
        except ValueError:
            print("Invalid letter found: " + letter)
            lettersFine = False
            break

    if not lettersFine:
        sys.exit(0)

    image = Image.new(mode="RGB", size=(len(letterNumbers), 3))

    for letterNumI in range(len(letterNumbers)):
        letterNum = letterNumbers[letterNumI]
        base3 = [math.floor(letterNum / 9), math.floor(letterNum / 3) % 3, letterNum % 3]
        image.putpixel((len(letterNumbers) - 1 - letterNumI, 0), colors[base3[2]])
        image.putpixel((len(letterNumbers) - 1 - letterNumI, 1), colors[base3[1]])
        image.putpixel((len(letterNumbers) - 1 - letterNumI, 2), colors[base3[0]])

    scalefactor = abs(int(input("how much you wants the scaling of each pixel ")))

    image = image.resize((scalefactor * len(letterNumbers), 3 * scalefactor), Image.Resampling.NEAREST)

    image.save(PATH + "/ciphered.png")
else:
    inputimage = input("what's the image name (relative to file, with file ext)? ")
    if not os.path.exists(PATH + "/" + inputimage) or inputimage == "":
        print("image not found")
        sys.exit(0)
    scalefactor = abs(int(input("how big is each color block? (integers only, put zero if you don't know, this will try to auto detect) ")))

    img = Image.open(PATH + "/" + inputimage)
    img = img.convert("RGBA")

    if scalefactor == 0:
        scalefactor = round(img.size[1] / 3)

    pixdata = img.load()
    width = round(img.size[0] / scalefactor)
    output = ""

    for letter in range(width):
        pixelX = img.size[0] - letter * scalefactor - 1
        pixelCols = []
        for pixCol in range(3):
            pixelCols.append(colors.index(pixdata[pixelX, pixCol * scalefactor]))
        output += textDictorany[pixelCols[2] * 9 + pixelCols[1] * 3 + pixelCols[0]]
    
    flags = "x"
    if os.path.exists(PATH + "/deciphered.txt"):
        flags = "w"
    file = open(PATH + "/deciphered.txt", flags)
    file.write(output)
    file.close()
    print("Deciphered has been written to deciphered.txt")