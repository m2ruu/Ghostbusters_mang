import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random

pygame.init()
ekraan = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ghostbusters')

# piltide määramine
taust = pygame.image.load('resources/image/background.png')
game_over = pygame.image.load('resources/image/gameover.png')

# mänguosad ja väljanägemine
fail1 = 'resources/image/a.png'
player_img = pygame.image.load(fail1)
fail2 = 'resources/image/b.png'
bullet_img = pygame.image.load(fail2)
fail3 = 'resources/image/c.png'
enemy_img = pygame.image.load(fail3)

# suurused
player_rect = []
player_rect.append(pygame.Rect(0, 0, 80,90))
player_pos = [200, 700]
player = Player(player_img, player_rect, player_pos)

bullet_rect = pygame.Rect(0, 0, 9, 10)
bullet_img = bullet_img.subsurface(bullet_rect)

enemy1_rect = pygame.Rect(0, 0, 100, 100)
enemy1_img = enemy_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(enemy_img.subsurface(pygame.Rect(0, 0, 100, 100)))

enemies1 = pygame.sprite.Group()
enemies_down = pygame.sprite.Group()

# kiirus
shoot_frequency = 0
enemy_frequency = 0

player_down_index = 50

score = 0

clock = pygame.time.Clock()

running = True

# main loop
while running:

    clock.tick(60)

    # mängija ei saa pihta, tulistab
    if not player.is_hit:
        if shoot_frequency % 30 == 0:
            player.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency >= 30:
            shoot_frequency = 0

    # enemy kiirusja palju teda on
    if enemy_frequency % 60 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    # bulleti väljumine ekraanilt
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    for enemy in enemies1:
        enemy.move()

        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            break
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies1.remove(enemy)

    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    ekraan.fill(0)
    ekraan.blit(taust, (0, 0))

    if not player.is_hit:
        ekraan.blit(player.image[0], player.rect)

        player.img_index = shoot_frequency // 1
    else:
        player.img_index = player_down_index // 8
        ekraan.blit(player.image[0], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            running = False

    # enemy skoorid ja värki
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            pass
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 10
            continue
        ekraan.blit(enemy_down.down_imgs[0], enemy_down.rect)
        enemy_down.down_index += 1

    player.bullets.draw(ekraan)
    enemies1.draw(ekraan)

    # tekstid lähevad ekraanile
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    ekraan.blit(score_text, text_rect)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    key_pressed = pygame.key.get_pressed()

    # playeri liikumine
    if not player.is_hit:
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()

font = pygame.font.Font(None, 48)
text = font.render('Score: ' + str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = ekraan.get_rect().centerx
text_rect.centery = ekraan.get_rect().centery + 24
ekraan.blit(game_over, (0, 0))
ekraan.blit(text, text_rect)

# saad mängu kinni panna
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()