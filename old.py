# video: the ultimate introduction to pygame

import pygame as pg
from sys import exit
from random import randint

pg.init()
screen = pg.display.set_mode((800, 400))
pg.display.set_caption('Runner')
#pg.display.set_icon ?

pg.font.init()

clock = pg.time.Clock()

run = 0

gravity = 0

global speed

speed = 5


background = pg.Surface((800, 400)).convert()
background.fill('Lightblue')
#ground = pg.Surface((800, 200)).convert()
#ground.fill('Brown')

ground = pg.image.load("assets/Constructionplatform-sprite1.png")
ground = pg.transform.scale(ground, (300, 300))
ground_rect = ground.get_rect(bottomleft = (0, 412))
print(ground_rect.left)
print(ground_rect.top)

#player = pg.Surface((20, 50)).convert()
#player.fill('Orange')
#player_rect = player.get_rect(bottomleft= (200, 300))

vijand = pg.Surface((20, 50)).convert()
vijand.fill("Black")
vijand_rect = vijand.get_rect(bottomleft = (1000, 300))

char = [pg.transform.scale(pg.image.load('assets/character_sprite1.png').convert_alpha(), (70, 70)), 
        pg.transform.scale(pg.image.load('assets/character_sprite2.png').convert_alpha(), (70, 70)), 
        pg.transform.scale(pg.image.load('assets/character_sprite3.png').convert_alpha(), (70, 70)), 
        pg.transform.scale(pg.image.load('assets/character_sprite4.png').convert_alpha(), (70, 70))]
char_rect = char[0].get_rect(bottomleft = (200, 300))

coin = pg.Surface((20, 20)).convert()
coin.fill("Yellow")
coin_rect = coin.get_rect(midleft = (1000, 265))

font = pg.font.SysFont("Sans Serif", 24)
coin_count = 0

obstacle_list = []

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for surface, rectangle in obstacle_list:
            rectangle.x -= speed

            screen.blit(surface, rectangle)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle[1].x > -100]

        return obstacle_list
    else: return []

def check_collision(obstacle_list, char_rect):
    if obstacle_list:
        for surface, rectangle in obstacle_list:
            if char_rect.colliderect(rectangle):
                # return false to set game active to false = game over
                # empty obstacle list to have a clean restart of the game
                # if it's a coin no game over but added coins
                pass


#timer

obstacle_timer = pg.USEREVENT + 1
pg.time.set_timer(obstacle_timer, 1500)




while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if char_rect.bottom == 300: # geen dubbeljump
                    gravity = -20
        if event.type == obstacle_timer:
            obstacles = [(vijand, vijand.get_rect(bottomleft = (randint(900, 1100), 300))), (coin, coin.get_rect(midleft = (randint(900, 1100), 265)))]
            obstacle_list.append(obstacles[randint(0, len(obstacles)-1)])
    
    if run + 1 >= 12:
        run = 0
    
    gravity += 1
    run += 1
    
    screen.blit(background, (0,0))
    screen.blit(ground, ground_rect)
    screen.blit(char[run//4], char_rect)
    screen.blit(vijand, vijand_rect)
    screen.blit(coin, coin_rect)
    coin_count_surface = font.render(str(coin_count), False, (0, 0, 0))
    screen.blit(coin_count_surface, (750, 50))
    #vijand_rect.left -= 0
    #if vijand_rect.right < 0: vijand_rect.left = 1000
    #
    #coin_rect.left -= 5
    #if coin_rect.right < 0: coin_rect.left = 1000

    if char_rect.colliderect(vijand_rect): 
        vijand_rect.left = 1000
    
    if char_rect.colliderect(coin_rect):
        coin_rect.left = 1000
        coin_count += 1

    char_rect.y += gravity
    if char_rect.bottom > 300:
        char_rect.bottom = 300

    # OBSTACLE SPAWNING
    obstacle_list = obstacle_movement(obstacle_list)
    check_collision(obstacle_list, char_rect)


    pg.display.update()
    clock.tick(60)

