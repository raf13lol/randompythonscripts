from PIL import Image
import os, math, PIL, sys
import PIL.ImageColor

images = []

# https://note.nkmk.me/en/python-pillow-add-margin-expand-canvas/
def add_margin(pil_img, top, right, bottom, left):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), (0, 0, 0, 0))
    result.paste(pil_img, (left, top))
    return result

lastpath = input("path to image? ")

while True:
    pathtrim = lastpath.removeprefix("\"")
    pathtrim = pathtrim.removesuffix("\"")
    if os.path.exists(pathtrim):
        image = Image.open(pathtrim)
        images.append(image)
        lastpath = input("path to another image? ")
    else:
        maxwidth = 0
        maxheight = 0
        for i in range(len(images)):
            maxwidth = max(images[i].size[0], maxwidth)
            maxheight = max(images[i].size[1], maxheight)

        for i in range(len(images)):
            widthmissing = maxwidth - images[i].size[0]
            heightmissing = maxheight - images[i].size[1]
            
            leftpart = math.ceil(widthmissing / 2)
            toppart = math.ceil(heightmissing / 2)

            widthmissing -= leftpart
            heightmissing -= toppart

            images[i] = add_margin(images[i], toppart, widthmissing, heightmissing, leftpart)
            
        images[0].save(f'C:/Users/{os.getenv("USERNAME")}/Downloads/{lastpath}.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0,
               transparency=0, disposal=2)
        break
