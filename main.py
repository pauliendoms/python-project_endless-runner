# video: the ultimate introduction to pygame
# https://www.youtube.com/watch?v=AY9MnQ4x3zk&list=PL8QF4nftNXtpnW24YpX9PjzSaHMJNGk7a&index=8&t=11341s
import pygame as pg
from sys import exit
from random import randint
from random import choice

pg.init()

class Player(pg.sprite.Sprite):
    def __init__(self):
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
    global upgrades
    global max_x

    def __init__(self):

        if not upgrades[1].bought:
            self.images = [pg.Surface((50, 50)).convert()]
            self.images[0].fill("Black")
        else:
            self.images = [pg.transform.scale(pg.image.load('assets/sawblade-1.png').convert_alpha(), (50, 50)), 
            pg.transform.scale(pg.image.load('assets/sawblade-2.png').convert_alpha(), (50, 50))]

        self.rect = self.images[0].get_rect(bottomleft = (randint(900, max_x), 300))
        self.rot = 0

    def blit(self):
        if upgrades[1].bought:
            if self.rot >= 10:
                self.rot = 0
            screen.blit(self.images[self.rot//5], self.rect)
            self.rot += 1
        else:
            screen.blit(self.images[0], self.rect)

class Coin():
    count = 0
    global upgrades
    global max_x

    def __init__(self):
        if not upgrades[2].bought:
            self.image = pg.Surface((20, 20)).convert()
            self.image.fill("Yellow")
        else:
            self.image = pg.image.load("assets/coin.png")
            self.image = pg.transform.scale(self.image, (20, 20))
        
        self.rect = self.image.get_rect(midleft = (randint(900, max_x), 265))

    def blit(self):
        screen.blit(self.image, self.rect)
    
    def collect():
        Coin.count += 1

    def blit_count():
        screen.blit(font.render("$" + str(Coin.count), False, (0, 0, 0)), (700, 20))

class Gap():
    global max_x

    def __init__(self):
        self.image = pg.Surface((100, 100)).convert()
        self.image.fill("Lightblue")
        self.rect = self.image.get_rect(topleft = (randint(900, max_x), 300))
    
    def blit(self):
        screen.blit(self.image, self.rect)

class Obstacle():
    def __init__(self, player):
        self.active_obstacles = []
        self.obstacles = [Coin, Enemy, Gap]
        self.player = player
        self.timer = 0
        self.generation_speed = 1500
    
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
        pg.time.set_timer(self.timer, self.generation_speed)
        
class Ground():
    global upgrades
    def __init__(self, x):
        if upgrades[0].bought:
            self.image = pg.image.load("assets/greenplatform.png")
            self.image = pg.transform.scale(self.image, (300, 300))
        else:
            self.image = pg.image.load("assets/Constructionplatform-sprite3.png")
            self.image = pg.transform.scale(self.image, (300, 300))
        
            
        self.x = x
        self.rect = self.image.get_rect(bottomleft = (self.x, 412))
    
    def blit(self, speed):
        if self.rect.right < 0:
            self.rect.left = 900 - speed - 20
        self.rect.left -= speed
        screen.blit(self.image, self.rect)

class Upgrade():
    def __init__(self, images, name, price, bought, number):
        self.images = []
        for i in images:
            self.images.append(pg.image.load(f"assets/{i}"))
        self.name = name
        self.price = price
        self.bought = bought
        self.number = number
    
    def buy(self):
        Coin.count -= self.price
        self.bought = 1
    
    def blit(self, x, y):
        screen.blit(self.images[0], (x, y))
        screen.blit(font.render(self.name, False, (0, 0, 0)), (x, y+50))
        if not self.bought:
            screen.blit(font.render("$" + str(self.price), False, (0, 0, 0)), (x, y+70))
            screen.blit(font.render(str(self.number), False, (0, 0, 0)), (x, y+90))
        else:
            screen.blit(font.render("Already bought", False, (0, 0, 0)), (x, y+70))
    
    def buyable(self):
        if Coin.count >= self.price:
            return True
        else:
            return False
        

screen = pg.display.set_mode((800, 400))
pg.display.set_caption('Work In Progress')
pg.display.set_icon(pg.image.load("assets/character_sprite1.png"))

pg.font.init()

clock = pg.time.Clock()

font = pg.font.SysFont("Sans Serif", 24)

background = pg.Surface((800, 400)).convert()
background.fill('Lightblue')

upgrades = [
    Upgrade(["greenplatform.png"], "Platform", 100, 0, 1),
    Upgrade(["sawblade-1.png", "sawblade-2.png"], "Enemy", 50, 0, 2),
    Upgrade(["coin.png"], "Coin", 10, 0, 3)
    ]

def initializePlay():
    player = Player()
    obstacle = Obstacle(player)
    ground = [Ground(0), Ground(300), Ground(600), Ground(900)]
    difficulty = 60
    max_x = 1100
    return (ground, player, obstacle, difficulty, max_x)

ground, player, obstacle, difficulty, max_x = initializePlay()

play = 0
highscore = 0


def Play():
    global highscore
    global difficulty
    global max_x
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
            if score > highscore:
                highscore = score

            bought_upgrades = 0
            for u in upgrades:
                if u.bought:
                    bought_upgrades += 1
            
            if bought_upgrades == len(upgrades):
                finish()
            
        score += 1
        screen.blit(font.render(str(score), False, (0, 0, 0)), (100, 20))
        screen.blit(font.render("Highscore: " + str(highscore), False, (0, 0, 0)), (200, 20))
        
        if score % 500 == 0:
            difficulty += 5
            obstacle.generation_speed -= 200
            max_x -= 10
        
        
        pg.display.update()
        clock.tick(difficulty)

def startMenu():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        global play
                        play = 1
                        return
                    if event.key == pg.K_s:
                        shop()
        screen.blit(background, (0, 0))
        screen.blit(font.render("menu", False, (0, 0, 0)),(380, 100))
        screen.blit(font.render("[Press space to play]", False, (0, 0, 0)),(330, 150))
        screen.blit(font.render("[Press S to go to the shop]", False, (0, 0, 0)),(320, 180))
        pg.display.update()

def shop():
    global ground
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    return
                for u in upgrades:
                    if pg.key.name(event.key) == u.number or pg.key.name(event.key) == "[" + str(u.number) + "]" or pg.key.key_code(pg.key.name(event.key)) == pg.key.key_code(str(u.number)):
                        if u.buyable():
                            u.buy()
                    
        screen.blit(background, (0, 0))
        screen.blit(font.render("shop", False, (0, 0, 0)),(380, 50))
        Coin.blit_count()
        x = 100
        for upgrade in upgrades:
            upgrade.blit(x, 150)
            x += 150

        screen.blit(font.render("[Press M to get back to the menu]", False, (0, 0, 0)),(320, 350))
        pg.display.update()

def finish():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            
        screen.blit(background, (0, 0))
        screen.blit(font.render("Congratulations!", False, (0, 0, 0)),(330, 100))
        screen.blit(font.render("You fixed the game!", False, (0, 0, 0)),(330, 150))
        screen.blit(font.render(f"Your final highscore is {highscore}", False, (0, 0, 0)),(320, 180))
        screen.blit(font.render("See if you can get a higher total highscore the next time you play!", False, (0, 0, 0)),(180, 210))
        pg.display.update()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    if play:
        ground, player, obstacle, difficulty, max_x = initializePlay()
        Play()
    else:
        startMenu();
    
        
