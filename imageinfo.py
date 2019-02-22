from PIL import Image, ImageEnhance, ImageFont, ImageDraw
import requests
from io import BytesIO


def enhanceImage(image, contrast=2.0):
    img = ImageEnhance.Contrast(image)
    img = img.enhance(contrast)
    return img


def sharpenImage(image, sharp=2.0):
    img = ImageEnhance.Sharpness(image)
    img = img.enhance(sharp)
    return img

def getImage(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def quantizetopalette(silf, palette, dither=False):  # did not write this function, might write it myself later

    silf.load()
    palette.load()
    if palette.mode != "P":
        raise ValueError("Bad mode")
    if silf.mode != "RGB" and silf.mode != "L":
        raise ValueError(
            "Only RGB or L"
            )
    im = silf.im.convert("P", 1 if dither else 0, palette.im)
    try:
        return silf._new(im)
    except AttributeError:
        return silf._makeself(im)


def addTj(image, bot, up):
    fontup = ImageFont.truetype('templates\\nangothic.ttf', 53) # tom and jerry function
    fontbt = ImageFont.truetype('templates\\nangothic.ttf', 40)
    txt = ImageDraw.Draw(image)
    txt.multiline_text((400, 250), up, font=fontup, fill=(0, 0, 0), align='center')
    txt.multiline_text((45, 520), bot, font=fontbt, fill=(0, 0, 0), align='center')
    return image


def addEb(image, one, two, three, four):
    font = ImageFont.truetype('templates\\nangothic.ttf', 40)   # brain meme template function
    txt = ImageDraw.Draw(image)
    txt.multiline_text((40, 55), one, font=font, fill=(0, 0, 0), align='center')
    txt.multiline_text((40, 330), two, font=font, fill=(0, 0, 0), align='center')
    txt.multiline_text((40, 655), three, font=font, fill=(0, 0, 0), align='center')
    txt.multiline_text((40, 935), four, font=font, fill=(0, 0, 0), align='center')
    return image




def textSplitter(text, maxline=2): # Might improve later but basic text wrapper for now
    words = text.split()
    count = 1
    wlist = []
    for word in words:
        if count % maxline == 0:
            wlist.append(word + '\n')
        else:
            wlist.append(word)
        count += 1
    space = " "
    space = space.join(wlist)
    return space
