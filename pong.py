import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', 'True')

import pygame
import random
import time

pygame.init()
random.seed()

class Player():
    def __init__(self):
        self.body = [(0,hgröse/2+i) for i in range(5)]
        self.dir = Direction.idle
        self.score = 0

    def move(self):
        for idx, body in enumerate(self.body):
            x, y = body
            ax, ay = self.dir

            nbody = (ax+x, ay+y)

            if ay+y < 0 or self.body[-1][1]+ay > hgröse-1:
                return

            self.body[idx] = nbody

    def draw(self):
            for body in self.body:
                x, y = body
                pygame.draw.rect(screen, Color.weis, (x*gröse, y*gröse, gröse, gröse))


class Player2(Player):
    def __init__(self):
        self.body = [(wgröse-1,hgröse/2+z) for z in range(5)]
        self.dir = Direction.idle
        self.score = 0

class Ball():
    def __init__(self):
        self.x = int(wgröse/2)
        self.y = int(hgröse/2)
        self.vector = Direction.idle

    def update_pos(self):
        if self.vector == Direction.idle:
            self.vector = random.choice(Direction.directions)
        self.x += self.vector[0]
        self.y += self.vector[1]

        if self.y not in range(1,hgröse-1):
            Sound.swall.play()
            if self.vector == Direction.directions[0]:
                self.vector = Direction.directions[2]
            elif self.vector == Direction.directions[2]:
                self.vector = Direction.directions[0]

            if self.vector == Direction.directions[1]:
                self.vector = Direction.directions[3]
            elif self.vector == Direction.directions[3]:
                self.vector = Direction.directions[1]

        elif self.x not in range(2,wgröse-2):
            if (self.x-1, self.y) in p1.body or (self.x+1, self.y) in p2.body:
                Sound.splayer.play()
                if self.vector == Direction.directions[3]:
                    self.vector = Direction.directions[2]
                elif self.vector == Direction.directions[2]:
                    self.vector = Direction.directions[3]

                if self.vector == Direction.directions[0]:
                    self.vector = Direction.directions[1]
                elif self.vector == Direction.directions[1]:
                    self.vector = Direction.directions[0]

            else:
                if self.x+self.vector[0] == 0:
                    p2.score += 1
                else:
                    p1.score += 1

                self.draw()
                self.x = int(wgröse/2)
                self.y = int(hgröse/2)
                self.vector = Direction.idle

                return True

    def draw(self):
        pygame.draw.rect(screen, Color.weis, (self.x*gröse, self.y*gröse, gröse, gröse))

    def display_score(self):
        pl1 = text_font.render(str(p1.score), False, Color.weis)
        pl2 = text_font.render(str(p2.score), False, Color.weis)
        screen.blit(pl1,(wgröse/2*gröse-5*gröse,hgröse/6*gröse))
        screen.blit(pl2,(wgröse/2*gröse+4*gröse,hgröse/6*gröse))

class Sound():
    swall = pygame.mixer.Sound("pong_wall.wav")
    splayer = pygame.mixer.Sound("pong1.wav")

class Color():
    weis = (255,255,255)
    schwarz = (0,0,0)
    rot = (255,0,0)

class Direction():
    idle = (0,0)
    up = (0,-1)
    down = (0,1)
    directions = ((-1,-1), (1,-1), (-1, 1), (1, 1))

def start_game():
    while True:
        startt = text_font.render("Insert Coin", False, Color.weis)
        screen.blit(startt,(wgröse/2.75*gröse,hgröse/3*gröse))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os._exit(1)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    screen.fill(Color.schwarz)
                    startt = text_font.render("Ready player one", False, Color.weis)
                    screen.blit(startt,(wgröse/3.5*gröse,hgröse/3*gröse))
                    pygame.display.update()
                    pygame.time.wait(2500)
                    return

        pygame.display.update()
        pygame.time.wait(500)
        screen.fill(Color.schwarz)
        pygame.display.update()
        pygame.time.wait(500)

def checkwinner():
    if p1.score == 10:
        return "Player one"
    elif p2.score == 10:
        return "Player two"

if __name__ == "__main__":

    wgröse = 80
    hgröse = 40

    gröse = 20

    width = wgröse * gröse
    height = hgröse * gröse
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")

    text_font = pygame.font.Font("PKMN RBYGSC.ttf", 50)

    firsttime = True

    p1 = Player()
    p2 = Player2()
    ball = Ball()

    clock = pygame.time.Clock()
    frames = 20

    oldtime = time.time()

    while True:
        while p1.score < 10 and p2.score < 10:
            clock.tick(frames)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os._exit(1)

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_w:
                        p1.dir = Direction.up

                    elif event.key == pygame.K_s:
                        p1.dir = Direction.down

                    elif event.key == pygame.K_UP:
                        p2.dir = Direction.up

                    elif event.key == pygame.K_DOWN:
                        p2.dir = Direction.down

                elif event.type == pygame.KEYUP:

                    if event.key == pygame.K_w:
                        p1.dir = Direction.idle

                    elif event.key == pygame.K_s:
                        p1.dir = Direction.idle

                    elif event.key == pygame.K_UP:
                        p2.dir = Direction.idle

                    elif event.key == pygame.K_DOWN:
                        p2.dir = Direction.idle

            screen.fill(Color.schwarz)

            if firsttime:
                start_game()
                firsttime = False

            p1.move()
            p2.move()
            p1.draw()
            p2.draw()
            if ball.update_pos():
                frames = 20
                oldtime = time.time()

            ball.draw()
            ball.display_score()

            if time.time() - oldtime >= 5:
                oldtime = time.time()
                frames += 1

            for i in range(hgröse):
                pygame.draw.rect(screen, Color.weis, (wgröse/2*gröse, 0+i*gröse, gröse/2, gröse/2))

            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os._exit(1)

        pygame.draw.rect(screen, Color.schwarz, (wgröse/2*gröse, 0, gröse, hgröse*gröse))
        winner = text_font.render("{} won!".format(checkwinner()), False, Color.weis)
        screen.blit(winner,(wgröse/3.5*gröse,hgröse/3*gröse))
        pygame.display.update()
