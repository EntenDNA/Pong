import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', 'True')

import pygame
import random
import time

pygame.init()
random.seed()

class Bot():
    def __init__(self):
        self.body = [(0,hgröse/2+i) for i in range(5)]
        self.dir = Direction.idle
        self.score = 0

    def move(self, rc):
        if ball.x < wgröse/2 or rc == 1:
            x, y = self.body[2]
            zdif = ball.y - y

            if zdif > 0:
                self.dir = (0, 1)
            elif zdif < 0:
                self.dir = (0, -1)

            for idx, body in enumerate(self.body):

                x, y = body
                ay = self.dir[1]
                nbody = (x, y+ay)

                if ay+y < 0 or self.body[-1][1]+ay > hgröse-1:
                    return

                self.body[idx] = nbody

    def draw(self):
            for body in self.body:
                x, y = body
                pygame.draw.rect(screen, Color.weis, (x*gröse, y*gröse, gröse, gröse))

class Bot2(Bot):
    def __init__(self):
        self.body = [(wgröse-1,hgröse/2+z) for z in range(5)]
        self.dir = Direction.idle
        self.score = 0

    def move(self, rc):
        if ball.x > wgröse/2 or rc == 1:
            x, y = self.body[2]
            zdif = ball.y - y

            if zdif > 0:
                self.dir = (0, 1)
            elif zdif < 0:
                self.dir = (0, -1)

            for idx, body in enumerate(self.body):

                x, y = body
                ay = self.dir[1]
                nbody = (x, y+ay)

                if ay+y < 0 or self.body[-1][1]+ay > hgröse-1:
                    return

                self.body[idx] = nbody

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
            if (self.x-1, self.y) in bot.body or (self.x+1, self.y) in bot2.body:
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
                    bot2.score += 1
                else:
                    bot.score += 1

                bot.body = [(0,hgröse/2+i) for i in range(5)]
                bot2.body = [(wgröse-1,hgröse/2+z) for z in range(5)]
                self.draw()
                self.x = int(wgröse/2)
                self.y = int(hgröse/2)
                self.vector = Direction.idle

                return True

    def draw(self):
        pygame.draw.rect(screen, Color.weis, (self.x*gröse, self.y*gröse, gröse, gröse))

    def display_score(self):
        pl1 = text_font.render(str(bot.score), False, Color.weis)
        pl2 = text_font.render(str(bot2.score), False, Color.weis)
        screen.blit(pl1,(wgröse/2*gröse-5*gröse-40,hgröse/6*gröse))
        screen.blit(pl2,(wgröse/2*gröse+5*gröse,hgröse/6*gröse))

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
    if bot.score == 10:
        return "Bot one"
    elif bot2.score == 10:
        return "Bot two"

if __name__ == "__main__":
    humanity = 4

    wgröse = 60
    hgröse = 40

    gröse = 20

    firsttime = True

    width = wgröse * gröse
    height = hgröse * gröse
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")

    text_font = pygame.font.Font("PKMN RBYGSC.ttf", 50)

    bot = Bot()
    bot2 = Bot2()
    ball = Ball()

    clock = pygame.time.Clock()
    frames = 20

    oldtime = time.time()

    while True:
        while bot.score < 10 and bot2.score < 10:
            clock.tick(frames)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os._exit(1)

            screen.fill(Color.schwarz)

            if firsttime:
                start_game()
                firsttime = False

            rc = random.randint(1,humanity)
            rc2 = random.randint(1,humanity)
            bot.move(rc)
            bot2.move(rc2)
            bot.draw()
            bot2.draw()
            if ball.update_pos():
                frames = 20
                oldtime = time.time()

            ball.draw()
            ball.display_score()

            if time.time() - oldtime >= 3:
                oldtime = time.time()
                frames += 1
            else:
                pass

            for i in range(hgröse):
                pygame.draw.rect(screen, Color.weis, (wgröse/2*gröse, i*gröse, gröse/2, gröse/2))

            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os._exit(1)

        pygame.draw.rect(screen, Color.schwarz, (wgröse/2*gröse, 0, gröse, hgröse*gröse))
        winner = text_font.render("{} won!".format(checkwinner()), False, Color.weis)
        screen.blit(winner,(wgröse/3.5*gröse,hgröse/3*gröse))
        pygame.display.update()
