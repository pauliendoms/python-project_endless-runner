# video: the ultimate introduction to pygame
# https://www.youtube.com/watch?v=AY9MnQ4x3zk&list=PL8QF4nftNXtpnW24YpX9PjzSaHMJNGk7a&index=8&t=11341s
import pygame as pg
from sys import exit
from random import randint
from random import choice

pg.init()

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [pg.transform.scale(pg.image.load('assets/character_sprite1.png').convert_alpha(), (70, 70)), 
        pg.transform.scale(pg.image.load('assets/character_sprite2.png').convert_alpha(), (70, 70)), 
        pg.transform.scale(pg.image.load('assets/character_sprite3.png').convert_alpha(), (70, 70)), 
        pg.transform.scale(pg.image.load('assets/character_sprite4.png').convert_alpha(), (70, 70))]
        self.rect = self.images[0].get_rect(bottomleft = (200, 300))
        self.run = 0
        self.gravity = 0
        print(type(self.images[0]))

    def move(self):
        if self.run + 1 >= 12:
            self.run = 0
        self.run += 1

    def blit(self):
        screen.blit(self.images[self.run//4], self.rect)

    def gravitate(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 300:
            self.rect.bottom = 300

    def jump(self):
        if self.rect.bottom == 300: # geen dubbeljump
                    self.gravity = -20

class Enemy():
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((20, 50)).convert()
        self.image.fill("Black")
        self.rect = (self.image).get_rect(bottomleft = (randint(900, 1100), 300))
    
    def blit(self):
        screen.blit(self.image, self.rect)

class Coin():
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((20, 20)).convert()
        self.image.fill("Yellow")
        self.rect = self.image.get_rect(midleft = (randint(900, 1100), 265))
        self.count = 0

    def blit(self):
        screen.blit(self.image, self.rect)
    
    def collect(self):
        self.count += 1
    
    def buy(self, prize):
        # de prize gaat van de coin_count af
        pass

class Obstacle():
    def __init__(self, player):
        self.active_obstacles = []
        self.obstacles = [Coin, Enemy]
        self.player = player
        self.timer = 0
    
    def new_obstacle(self):
        self.active_obstacles.append(choice(self.obstacles)())

    def move(self):
        if self.active_obstacles:
            for obstacle in self.active_obstacles:
                obstacle.rect.x -= speed

                obstacle.blit()

            self.active_obstacles = [obstacle for obstacle in self.active_obstacles if obstacle.rect.x > -100]

    def collision(self):
        if self.active_obstacles:
            for obstacle in self.active_obstacles:
                if self.player.rect.colliderect(obstacle.rect):
                    # return false to set game active to false = game over
                    # empty obstacle list to have a clean restart of the game
                    # if it's a coin no game over but added coins
                    pass # I tested with a print statement: collision are detected
    
    def timing(self):
        self.timer = pg.USEREVENT + 1
        pg.time.set_timer(self.timer, 1500)
        

screen = pg.display.set_mode((800, 400))
pg.display.set_caption('Runner')
#pg.display.set_icon ?

pg.font.init()

clock = pg.time.Clock()

global speed

speed = 5

background = pg.Surface((800, 400)).convert()
background.fill('Lightblue')

ground = pg.image.load("assets/Constructionplatform-sprite1.png")
ground = pg.transform.scale(ground, (300, 300))
ground_rect = ground.get_rect(bottomleft = (0, 412))
# print(ground_rect.left) -> 0
# print(ground_rect.top) -> 112

player = Player()
obstacle = Obstacle(player)

#font = pg.font.SysFont("Sans Serif", 24)

#timer

obstacle.timing()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.jump()
        if event.type == obstacle.timer:
            obstacle.new_obstacle()

    player.move()
    
    player.gravitate()
    
    screen.blit(background, (0,0))
    screen.blit(ground, ground_rect)
    player.blit()
    #coin_count_surface = font.render(str(coin_count), False, (0, 0, 0))

    # OBSTACLE SPAWNING
    obstacle.move()
    obstacle.collision()


    pg.display.update()
    clock.tick(60)

