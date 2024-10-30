from PIL import Image

image = Image.new("RGB", (256, 128))

def rgb555torgb888(col):
    return (int(col[0] / 31 * 255), int(col[1] / 31 * 255), int(col[2] / 31 * 255))

bigfatarray = []

posx = 0
posy = 0

for b in range(32):
    for g in range(32):
        for r in range(32):
            col = rgb555torgb888([r, g, b])
            image.putpixel([posx, posy], col)
            if col in bigfatarray:
                print("die")

            bigfatarray.append(col)
            posx += 1
            if posx >= 256:
                posx = 0
                posy += 1

image.save("image.png")