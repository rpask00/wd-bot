from PIL import Image, ImageGrab
from pynput.mouse import Button, Controller
import time
import random
import pickle

ALL = []

def try_resolve():
    for imag in range(1, 22):
        im = Image.open(f'tries/ready/try_{imag}.PNG')
        pix = im.load()
        pixel = pix[750, 315][0:3]
        if pixel != (169, 1, 0):
            return

        colors = []

        for j in range(2):
            for i in range(3):
                piks = []
                for a in range(6):

                    x = 924 + i * 128
                    y = 348 + j * 128 + a*16

                    color = pix[x, y][0:3]
                    piks.append(color)

                colors.append(tuple(piks))

        puz = {}
        for i, color in enumerate(colors):
            puz[color] = i

        ALL.append(puz)

    with open('puz.txt', 'wb') as f:
        pickle.dump(ALL, f)


try_resolve()


print(ALL)
