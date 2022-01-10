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

    def move(self):
        if self.run + 1 >= 12:
            self.run = 0
        self.run += 1

    def blit(self):
        screen.blit(self.images[self.run//4], self.rect)

    def gravitate(self, limit):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > limit:
            self.rect.bottom = limit

    def jump(self):
        if self.rect.bottom == 300: # geen dubbeljump
            self.gravity = -17

class Enemy():
    def __init__(self):
        super().__init__()
        #self.image = pg.image.load("assets/sawblade-1.png")
        #self.image = pg.transform.scale(self.image, (50, 50))

        #self.image = pg.Surface((50, 50)).convert()
        #self.image.fill("Black")
        #self.rect = (self.image).get_rect(bottomleft = (randint(900, 1100), 300))

        self.images = [pg.transform.scale(pg.image.load('assets/sawblade-1.png').convert_alpha(), (50, 50)), 
        pg.transform.scale(pg.image.load('assets/sawblade-2.png').convert_alpha(), (50, 50))]
        self.rect = self.images[0].get_rect(bottomleft = (randint(900, 1100), 300))
        self.rot = 0

    #def rotate(self):
    #    if self.rot + 1 >= 6:
    #        self.rot = 0
    #    self.rot += 1

    def blit(self):
        if self.rot >= 10:
            self.rot = 0
        screen.blit(self.images[self.rot//5], self.rect)
        self.rot += 1
    
    #def blit(self):
        #screen.blit(self.image, self.rect)

class Coin():
    count = 0
    def __init__(self):
        super().__init__()
        #self.image = pg.Surface((20, 20)).convert()
        self.image = pg.image.load("assets/coin.png")
        self.image = pg.transform.scale(self.image, (20, 20))
        #self.image.fill("Yellow")
        self.rect = self.image.get_rect(midleft = (randint(900, 1100), 265))

    def blit(self):
        screen.blit(self.image, self.rect)
    
    def collect():
        Coin.count += 1

    def blit_count():
        screen.blit(font.render(str(Coin.count), False, (0, 0, 0)), (700, 20))

    def buy(self, prize):
        # de prize gaat van de coin_count af
        pass

class Gap():
    def __init__(self):
        self.image = pg.Surface((100, 100)).convert()
        self.image.fill("Lightblue")
        self.rect = self.image.get_rect(topleft = (randint(900, 1100), 300))
    
    def blit(self):
        screen.blit(self.image, self.rect)

class Obstacle():
    def __init__(self, player):
        self.active_obstacles = []
        self.obstacles = [Coin, Enemy, Gap]
        self.player = player
        self.timer = 0
    
    def new_obstacle(self):
        self.active_obstacles.append(choice(self.obstacles)())

    def move(self, speed):
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
                    # I tested with a print statement: collision are detected
                    if type(obstacle) == Coin:
                        Coin.collect()
                        self.active_obstacles.remove(obstacle)
                        return True
                    elif type(obstacle) == Enemy:
                        if self.player.rect.right >= obstacle.rect.left + 15 and self.player.rect.left <= obstacle.rect.right - 15 and self.player.rect.bottom >= obstacle.rect.top:
                            return False
                
                if type(obstacle) == Gap:
                    if self.player.rect.right > obstacle.rect.left + 35 and self.player.rect.left < obstacle.rect.right - 35:
                        if self.player.rect.bottom >= 300:
                            return False
        return True

    def terminate(self):
        if self.active_obstacles:
            for obstacle in self.active_obstacles:
                if obstacle.rect.right < 0:
                    self.active_obstacles.remove(obstacle)

    
    def timing(self):
        self.timer = pg.USEREVENT + 1
        pg.time.set_timer(self.timer, 1500)
        
class Ground():
    def __init__(self, x):
        #self.image = pg.image.load("assets/Constructionplatform-sprite3.png")
        self.image = pg.image.load("assets/greenplatform.png")
        self.image = pg.transform.scale(self.image, (300, 300))
        self.x = x
        self.rect = self.image.get_rect(bottomleft = (self.x, 412))
    
    def blit(self, speed):
        if self.rect.right < 0:
            self.rect.left = 900 - speed - 20
        self.rect.left -= speed
        screen.blit(self.image, self.rect)            

screen = pg.display.set_mode((800, 400))
pg.display.set_caption('Runner')
#pg.display.set_icon ?

pg.font.init()

clock = pg.time.Clock()

font = pg.font.SysFont("Sans Serif", 24)

background = pg.Surface((800, 400)).convert()
background.fill('Lightblue')

def initializePlay():
    ground = [Ground(0), Ground(300), Ground(600), Ground(900)]
    player = Player()
    obstacle = Obstacle(player)
    return (ground, player, obstacle);

ground, player, obstacle = initializePlay()

play = 0

def Play():
    speed = 5
    obstacle.timing()

    score = 0
    running = True

    while running:
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

        player.gravitate(300)

        screen.blit(background, (0,0))
        for i in ground:
            i.blit(speed)

        player.blit()
        Coin.blit_count()

        # OBSTACLE SPAWNING
        obstacle.move(speed)
        obstacle.terminate()
        running = obstacle.collision()
        global play
        play = 0
        if not running and type(obstacle.active_obstacles[0]) == Gap:
            player.gravitate(400)
            blue = pg.Surface((800 , 100))
            blue.fill("Lightblue")
            screen.blit(blue, (0, 200))
            player.blit()
        
        if not running:
            obstacle.active_obstacles = []

        score += 1
        screen.blit(font.render(str(score), False, (0, 0, 0)), (100, 20))
        
        #if score % 1000 == 0:
        #    speed += 2
        pg.display.update()
        clock.tick(60)

def startMenu():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                    print("here we are now")
                    if event.key == pg.K_SPACE:
                        print("entertain us")
                        global play
                        play = 1
                        return
        screen.blit(background, (0, 0))
        screen.blit(font.render("menu", False, (0, 0, 0)),(380, 100))
        screen.blit(font.render("[Press space to play]", False, (0, 0, 0)),(330, 150))
        pg.display.update()

def shop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                pass
        screen.blit(background, (0, 0))
        screen.blit(font.render("menu", False, (0, 0, 0)),(380, 100))
        screen.blit(font.render("[Press space to play]", False, (0, 0, 0)),(330, 150))
        pg.display.update()

while True:
    for event in pg.event.get():
        print(event.type)
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    print(play)
    if play:
        initializePlay()
        Play()
    else:
        startMenu();
    
        
