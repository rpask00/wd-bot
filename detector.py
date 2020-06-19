from PIL import Image, ImageGrab
from pynput.mouse import Button, Controller
import time
import random
import pickle

pygame.init()
gui = Gui()
surface = pygame.display.set_mode((800, 800))
pygame.display.set_caption('War of Dragons ')
programIcon = pygame.image.load('wd.gif')
pygame.display.set_icon(programIcon)


koniczyna = set([(255, 52, 250), (255, 154, 255), (255, 20, 241),
                 (255, 90, 241), (255, 134, 255), (255, 64, 228), (255, 53, 255), (255, 76, 246), (255, 3, 241)])
oset = set([(231, 56, 50), (54, 139, 20), (174, 200, 92),
            (152, 202, 118), (110, 150, 48), (222, 192, 100)])
jemiola = set([(4, 0, 30)])
grey_fish = set([(192, 199, 238), (111, 107, 147), (118, 114, 152)])
milfoil = set([(92, 151, 209)])
irys = set([(167, 114, 0), (255, 229, 7), (80, 120, 53)])
rozmaryn = set([(31, 78, 135), (81, 173, 52), (90, 167, 255)])
ogiennik = set([(255, 245, 0), (253, 236, 0)])
lotos = set([(144, 90, 107), (186, 46, 94)])
nasienie = set([(125, 38, 96), (81, 28, 81)])

all_flowers = jemiola.union(koniczyna.union(oset))


class Flower:
    def __init__(self, colors, lvl):
        self.colors = colors
        self.lvl = lvl

    def cut_flower(self, position):
        self.mouse = Controller()
        self.mouse.position = position
        self.mouse.click(Button.left, 2)


class Fight:
    def __init__(self, lvl):
        self.lvl = lvl
        self.mouse = Controller()
        self.combo = [2, 3, 3, 3]
        self.eliksir_position = 0

    def got_to_battlefield(self):
        self.mouse = Controller()
        self.mouse.position = 940, 140
        self.mouse.click(Button.left, 1)
        time.sleep(1)
        press_cancel()

    def strike(self, attack_direction):
        print(attack_direction)
        if attack_direction == 1:
            self.mouse.position = 500, 380
        elif attack_direction == 2:
            self.mouse.position = 525, 425
        else:
            self.mouse.position = 505, 465

        self.mouse.click(Button.left, 1)

    def block(self):
        time.sleep(2)
        self.mouse.position = 425, 420
        self.mouse.click(Button.left, 1)

    def health_check(self):
        take_screenshoot()
        im = Image.open('img/source.PNG')
        pix = im.load()

        return pix[348, 233] == (38, 0, 0)

    def eliksir(self):
        potions = [
            (30, 225),
            (30, 270),
            (30, 320),
            (30, 350),
            (30, 380),
            (30, 410),
            (30, 440),
        ]

        print(potions[self.eliksir_position])
        self.mouse.position = potions[self.eliksir_position]
        self.eliksir_position += 1
        self.mouse.click(Button.left, 1)
        time.sleep(6)

    def call_covrus(self):
        self.mouse.position = 1890, 310
        self.mouse.click(Button.left, 1)
        time.sleep(1)
        self.mouse.position = 260, 225
        self.mouse.click(Button.left, 1)
        time.sleep(1)

    def fight(self):
        take_screenshoot()
        im = Image.open('img/source.PNG')
        pix = im.load()

        if pix[485, 210] != (111, 27, 27):
            return False

        if self.lvl is 2:
            self.call_covrus()
            while check_fight_status() is not 1:
                time.sleep(1)
            self.block()

        while True:
            fight_status = check_fight_status()

            if fight_status == 1:
                if not self.combo:
                    self.combo = [2, 3, 3, 3]

                if self.health_check():
                    self.eliksir()

                self.strike(self.combo.pop())
                time.sleep(3)

            if fight_status == 2:
                self.eliksir_position = 0
                break

        self.got_to_battlefield()

        return True


X_MIN = 200
X_MAX = 1700

Y_MIN = 170
Y_MAX = 1015

COUNT = 0

positions = {
    0: (924, 410),
    1: (1052, 410),
    2: (1180, 410),
    3: (924, 538),
    4: (1052, 538),
    5: (1180, 538)
}

with open('puz.txt', 'rb') as f:
    puzzle_palettes = pickle.load(f)


def pasek_stanu_status():
    take_screenshoot()
    im = Image.open('img/source.PNG')
    pix = im.load()

    return pix[1105, 506] == (187, 50, 50)


def get_puzzles_order(colors):
    selected = 0
    for palette in puzzle_palettes:
        didBreak = False
        for color in colors:
            if color not in palette:
                didBreak = True
                break

        if not didBreak:
            selected = palette
            break

    if selected is not 0:
        return [selected[color] for color in colors]


def move_puzzle(from_, to_, array):
    print(from_, to_)
    temp = array[from_]
    array[from_] = array[to_]
    array[to_] = temp

    mouse = Controller()
    mouse.position = positions[from_]
    mouse.press(Button.left)
    mouse.position = positions[to_]
    mouse.release(Button.left)


def press_ok():
    mouse = Controller()
    mouse.position = (760, 480)
    mouse.click(Button.left)


def append_puzzle(puz):
    with open('puz.txt', 'rb') as f:
        data = pickle.load(f)
        data.append(puz)

    with open('puz.txt', 'wb') as f:
        pickle.dump(data, f)
        print(data)


def try_resolve():
    im = Image.open('img/source.PNG')
    pix = im.load()
    if pix[750, 315] != (169, 1, 0):
        return

    sample = ImageGrab.grab()
    sample.save(f'img/try_{random.randint(0,10000)}.PNG')

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

    colors = get_puzzles_order(colors)

    if not colors:
        print('no color found')
        return

    while colors != [0, 1, 2, 3, 4, 5]:
        for i, c in enumerate(colors):
            if i == c:
                continue

            move_puzzle(i, c, colors)
            time.sleep(1)

    press_ok()


def check_status():
    take_screenshoot()
    im = Image.open('img/source.PNG')
    pix = im.load()

    if pix[955, 515] == (255, 0, 0) or pix[950, 462] == (255, 0, 0):
        return 1

    if pix[840, 440] == (125, 0, 0):
        return 2

    if pix[856, 531] == (255, 0, 0):
        return 3

    return False


def find_position(flower, direction):
    im = Image.open('img/source.PNG')
    pix = im.load()

    if direction == 1:
        for x in range(X_MIN, X_MAX):
            for y in range(Y_MIN, Y_MAX):
                if pix[x, y] in flower:
                    return x, y
    else:
        for x in range(X_MAX, X_MIN, -1):
            for y in range(Y_MIN, Y_MAX):
                if pix[x, y] in flower:
                    return x, y


def take_screenshoot():
    im = ImageGrab.grab()
    im.save('img/source.PNG')
    time.sleep(.5)


def press_cancel(mode=1):
    if not mode:
        return False
    mouse = Controller()

    positions = [(960, 490), (950, 530), (960, 510)]

    for i in range(3):
        mouse.position = (positions[i])
        mouse.click(Button.left, 1)
        time.sleep(.1)

    return mode


def check_fight_status():
    take_screenshoot()
    im = Image.open('img/source.PNG')
    pix = im.load()

    if pix[485, 420] == (22, 53, 86):
        return 1

    if pix[485, 420] == (30, 8, 5):
        return 2

    return 0


def scroll_screen(direction):
    mouse = Controller()
    if direction == 1:
        mouse.scroll(0, 1000)
    else:
        mouse.scroll(0, -1000)


flower = Flower(nasienie, 1)
fight = Fight(flower.lvl)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            COUNT += 1
            
    while True:
        take_screenshoot()
        time.sleep(1)
        fight.fight()
        try_resolve()

        position = find_position(flower.colors, COUNT % 2)
        if position:
            break

        press_cancel()

        scroll_direction = random.randint(0, 1)
        for i in range(random.randint(5, 15)):
            scroll_screen(scroll_direction)
            time.sleep(0.1)

    flower.cut_flower(position)

    time.sleep(3)

    # if press_cancel(check_status()):
    #     continue

    iterator = 0
    while pasek_stanu_status():
        iterator += 1
        if fight.fight() or iterator > 60:
            break

    time.sleep(4)

    press_cancel()
