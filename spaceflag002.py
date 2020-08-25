import pygame
from glob import glob
import random

size = w, h = 400, 600
screen = pygame.display.set_mode((size), 32, 1)
pygame.display.set_caption("Flappy Py")



class Sprite(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        global g
        super(Sprite, self).__init__()
        self.x = x
        self.y = y
        self.frames = [load(f[:-4]) for f in glob(file + "*.png")]
        self.image = self.frames[0]
        w, h = self.image.get_size()
        self.rect = pygame.Rect(self.x, self.y, w, h)
        self.cnt = 0
        self.mask = pygame.mask.from_surface(self.image)
        g.add(self)

    def update(self):
        global pipes
        global moveup, gameover
        # when moveup animation's faster
        if not moveup:
            self.cnt += .1
        if self.cnt > len(self.frames) - 1:
            self.cnt = 0
        self.image = self.frames[int(self.cnt)]
        for pipe in pipes:
            if pygame.sprite.collide_mask(pipe, self):
                print("touched")
                gameover = 1


class Bg(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        global g
        super(Bg, self).__init__()
        self.x = x
        self.y = y
        self.image = load(file)
        w, h = self.image.get_size()
        self.rect = pygame.Rect(self.x, self.y, w, h)
        g.add(self)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, file, x, y, pos=0):
        super(Pipe, self).__init__()
        global g, pipes

        self.pos = pos
        self.x = x + 300
        self.y = random.randint(450, 550)
        if pos == 0:
            self.image = load(file)
            w, h = self.image.get_size()
            self.rect = pygame.Rect(self.x, self.y, w, h)
        else:
            # self.y = random.randint(-400, -200)
            self.image = flip(file)
            w, h = self.image.get_size()
            self.rect = pygame.Rect(self.x, self.y, w, h)
            self.rect.bottom = random.randint(250, 300)
        self.mask = pygame.mask.from_surface(self.image)
        self.counter = 0
        pipes.add(self)
        g.add(self)

    def update(self):
        global score
        if random.random() > .5:
            movement = random.randrange(-5, -1)
        else:
            movement = random.randrange(1, 5)
        self.counter += 1
        if int(self.counter) % 5 == 0:
            if self.pos == 0:
                self.rect.top += movement
            else:
                self.rect.bottom += movement
        
        score += 1
        self.rect.left -= 1
        if self.rect.left < -100:
            self.rect.left = 400
            self.y = random.randint(450, 550)


class Base(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        global g

        super(Base, self).__init__()
        self.x = x
        self.y = y
        self.image = load(file)
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        g.add(self)

    def update(self):
        self.rect.left -= 1
        if self.rect.left < -400:
            self.rect.left = 399


def load(file):
    return pygame.image.load(file + ".png")


def flip(file):
    return pygame.transform.flip(pygame.image.load(file + ".png"), 0, 1)


def gravity():
    flappy.rect.top += 1


def start():
    global g, pipes, flappy, score

    score = 0
    g = pygame.sprite.Group()
    Bg("sky2", 0, 0)
    flappy = Sprite("ship8", 50, 300)
    pipes = pygame.sprite.Group()
    Pipe("pipe-green", 100, 300, 0)
    Pipe("pipe-green", 200, 300, 0)
    Pipe("pipe-green", 300, 300, 0)
    Pipe("pipe-green", 400, 300, 0)
    Pipe("pipe-green", 500, 300, 0)
    Pipe("pipe-green", 100, 0, 1)
    Pipe("pipe-green", 200, 0, 1)
    Pipe("pipe-green", 300, 0, 1)
    Pipe("pipe-green", 400, 0, 1)
    Pipe("pipe-green", 500, 0, 1)

    Base("base", 400, 550)
    Base("base", 0, 550)
    main()


def main():
    global moveup, gameover
    global g, pipes, flappy, score

    # jump controlo variables:
    # - after you press
    moveup = 0
    gameover = 0
    # how high can go
    startcounter = 0
    # How hight flappy jumps
    topjump = 20
    # how speed it jumps
    jumpspeed = 2
    screen.fill((0,0,0))
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    loop = 1
    while loop:

        if moveup:
            flappy.rect.top -= jumpspeed
            startcounter += 1
            # fly faster
            flappy.cnt += .5
            # print(startcounter)
        if startcounter == topjump:
            startcounter = 0
            moveup = 0

        if gameover:
            moveup = 0
            flappy.rect.top += 1
            flappy.cnt += 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    moveup = 1
                    startcounter = 1
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                if event.key == pygame.K_s:
                    flappy.rect.top = 300
                    start()

        if not gameover:
            g.draw(screen)
            g.update()
            if not moveup:
                gravity()
            pygame.display.update()
            clock.tick(120)


    pygame.quit()


start()


