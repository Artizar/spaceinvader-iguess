import random
import winsound

import pygame
import math


pygame.init()
width = 1000
height = 650
screen = pygame.display.set_mode((width,height))
timer = pygame.time.Clock()
fps = 60
bg = pygame.image.load('SPACE_Background.jpeg').convert_alpha()
bg = pygame.transform.scale(bg,(width,height))

level1 = pygame.image.load('spacelevel-1.jpeg').convert_alpha()
level1 = pygame.transform.scale(level1, (width,height))

level2 = pygame.image.load('spacelevel-2.jpeg').convert_alpha()
level2 = pygame.transform.scale(level2, (width,height))

level3 = pygame.image.load('spacelevel-3.jpeg').convert_alpha()
level3 = pygame.transform.scale(level3, (width,height))




playering = pygame.image.load('player.png')
playering = pygame.transform.scale(playering,(60,60))
playerX_pos = 470
playerY_pos = 550
player_vel = 0

bulletimg = pygame.image.load('bullet1.png').convert_alpha()
bulletimg = pygame.transform.scale(bulletimg,(20,40))
bulletX = playerX_pos
bulletY = playerY_pos
bulletY_change = 10
bulletstate = "ready"

score_value = 0
font = pygame.font.SysFont('comisan', 25)

enemy_img = []
enemyX_pos = []
enemyY_pos = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 5

for a in range(num_of_enemy):
    enemyimg = pygame.image.load('enemy.png')
    enemyimg = pygame.transform.scale(enemyimg,(60,60))
    enemy_img.append(enemyimg)
    enemyX_pos.append(random.randint(10,930))
    enemyY_pos.append(random.randint(0, 200))
    enemyX_change.append(random.randint(1, 5))
    enemyY_change.append(60)

def show_enemy(enemyX_pos, enemyY_pos,a):
    screen.blit(enemy_img[a],(enemyX_pos,enemyY_pos))


def firebullet(x,y):
    global bulletstate
    bulletstate = "fire"
    screen.blit(bulletimg,(x+20,y))

def hit(bulletX,bulletY,enemyX_pos,enemyY_pos):
    distance = math.sqrt((math.pow(enemyX_pos - bulletX, 2)) + (math.pow(enemyY_pos - bulletY, 2)))
    if distance < 30:
        return True
    else:
        return False

def hit_test(playerX_pos,playerY_pos,enemyX_pos,enemyY_pos):
    distance = math.sqrt((math.pow(enemyX_pos - playerX_pos, 2)) + (math.pow(enemyY_pos - playerY_pos, 2)))
    if distance < 30:
        return True
    else:
        return False


def show_score(x,y):
    score_text = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

while True:
    screen.blit(bg, (0, 0))
    if score_value > 33:
      screen.blit(level1,(0,0))
    if score_value > 66:
        screen.blit(level2, (0,0))
    if score_value > 99:
        screen.blit(level3, (0,0))
    screen.blit(playering,(playerX_pos,playerY_pos))
    for a in range(num_of_enemy):
        show_enemy(enemyX_pos[a], enemyY_pos[a], a)
        enemyX_pos[a] += enemyX_change[a]
        if enemyX_pos[a] > 950:
            enemyY_pos[a] += enemyY_change[a]
            enemyX_change[a] = enemyX_change[a] * -1
        if enemyX_pos[a] < 5:
            enemyY_pos[a] += enemyY_change[a]
            enemyX_change[a] = enemyX_change[a] * -1
        is_touch = hit_test(playerX_pos, playerY_pos,enemyX_pos[a], enemyY_pos[a])
        if is_touch:
            pygame.quit()
        is_hit = hit(bulletX, bulletY, enemyX_pos[a], enemyY_pos[a])
        if is_hit:
            bulletstate = "ready"
            winsound.PlaySound('sf-fb.wav',winsound.SND_ASYNC)
            enemyX_pos[a] = random.randint(10, 930)
            enemyY_pos[a] = random.randint(0, 200)
            score_value +=  1
            bulletX = playerX_pos
            bulletY = playerY_pos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_vel = -5
            if event.key == pygame.K_d:
                player_vel = 5
            if event.key == pygame.K_SPACE:
                if bulletstate == 'ready':
                    bulletX = playerX_pos
                    firebullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            player_vel = 0
    if bulletstate == "fire":
        firebullet(bulletX,bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = playerY_pos
        bulletX = playerX_pos + 20
        bulletstate = 'ready'
    show_score(10, 10)
    playerX_pos +=  player_vel
    bulletX_pos = playerX_pos + 20

    playerX_pos += player_vel
    bulletX = playerX_pos + 20
    if playerX_pos > 950:
        playerX_pos -= player_vel
    if playerX_pos < 5:
        playerX_pos =- player_vel
    timer.tick(fps)
    pygame.display.update()
screen.update()