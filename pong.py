import pygame
import os
import random
import time
pygame.init()
random.seed()

weis = (255,255,255)
schwarz = (0,0,0)
rot = (255,0,0)

global frames
frames = 20

wgröse = 70
hgröse = 40

gröse = 20

width = wgröse * gröse
height = hgröse * gröse
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

POKEFONT = pygame.font.Font("PKMN RBYGSC.ttf", 50)

idle = (0,0)
up = (0,-1)
down = (0,1)
directions = ((-1,-1), (1,-1), (-1, 1), (1, 1))

swall = pygame.mixer.Sound("pong_wall.wav")
splayer = pygame.mixer.Sound("pong1.wav")

firsttime = True

class Player():
    def __init__(self):
        self.body = [(0,hgröse/2+i) for i in range(5)]
        self.dir = idle
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
                pygame.draw.rect(screen, weis, (x*gröse, y*gröse, gröse, gröse))


class Player2(Player):
    def __init__(self):
        self.body = [(wgröse-1,hgröse/2+z) for z in range(5)]
        self.dir = idle
        self.score = 0

class Ball():
    def __init__(self):
        self.x = int(wgröse/2)
        self.y = int(hgröse/2)
        self.vector = (1,1)

    def update_pos(self):
        if self.vector == idle:
            self.vector = random.choice(directions)
        self.x += self.vector[0]
        self.y += self.vector[1]

        if self.y not in range(1,hgröse-1):
            swall.play()
            if self.vector == directions[0]:
                self.vector = directions[2]
            elif self.vector == directions[2]:
                self.vector = directions[0]

            if self.vector == directions[1]:
                self.vector = directions[3]
            elif self.vector == directions[3]:
                self.vector = directions[1]

        elif self.x not in range(2,wgröse-2):
            if (self.x+self.vector[0], self.y+self.vector[1]) in p1.body or (self.x+self.vector[0], self.y+self.vector[1]) in p2.body:
                splayer.play()
                if self.vector == directions[3]:
                    self.vector = directions[2]
                elif self.vector == directions[2]:
                    self.vector = directions[3]

                if self.vector == directions[0]:
                    self.vector = directions[1]
                elif self.vector == directions[1]:
                    self.vector = directions[0]

            else:
                if self.x+self.vector[0] == 0:
                    p2.score += 1
                else:
                    p1.score += 1

                self.draw()
                self.x = int(wgröse/2)
                self.y = int(hgröse/2)
                self.vector = idle

                return True

    def draw(self):
        pygame.draw.rect(screen, weis, (self.x*gröse, self.y*gröse, gröse, gröse))

    def display_score(self):
        pl1 = POKEFONT.render(str(p1.score), False, weis)
        pl2 = POKEFONT.render(str(p2.score), False, weis)
        screen.blit(pl1,(wgröse/2*gröse-5*gröse,hgröse/6*gröse))
        screen.blit(pl2,(wgröse/2*gröse+4*gröse,hgröse/6*gröse))

def start_game():
    while True:
        startt = POKEFONT.render("Insert Coin", False, weis)
        screen.blit(startt,(wgröse/2.75*gröse,hgröse/3*gröse))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os._exit(1)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    screen.fill(schwarz)
                    startt = POKEFONT.render("Ready player one", False, weis)
                    screen.blit(startt,(wgröse/3.5*gröse,hgröse/3*gröse))
                    pygame.display.update()
                    pygame.time.wait(2500)
                    return

        pygame.display.update()
        pygame.time.wait(500)
        screen.fill(schwarz)
        pygame.display.update()
        pygame.time.wait(500)

def checkwinner():
    if p1.score == 10:
        return "Player one"
    elif p2.score == 10:
        return "Player two"

p1 = Player()
p2 = Player2()
ball = Ball()

clock = pygame.time.Clock()
oldtime = time.time()

while True:
    while p1.score < 10 and p2.score < 10:
        print(frames)
        clock.tick(frames)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os._exit(1)

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    p1.dir = up

                elif event.key == pygame.K_s:
                    p1.dir = down

                elif event.key == pygame.K_UP:
                    p2.dir = up

                elif event.key == pygame.K_DOWN:
                    p2.dir = down

            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_w:
                    p1.dir = idle

                elif event.key == pygame.K_s:
                    p1.dir = idle

                elif event.key == pygame.K_UP:
                    p2.dir = idle

                elif event.key == pygame.K_DOWN:
                    p2.dir = idle

        screen.fill(schwarz)

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
        else:
            pass

        for i in range(hgröse):
            pygame.draw.rect(screen, weis, (wgröse/2*gröse, 0+i*gröse, gröse/2, gröse/2))

        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os._exit(1)

    pygame.draw.rect(screen, schwarz, (wgröse/2*gröse, 0, gröse, hgröse*gröse))
    winner = POKEFONT.render("{} won!".format(checkwinner()), False, weis)
    screen.blit(winner,(wgröse/3.5*gröse,hgröse/3*gröse))
    pygame.display.update()
