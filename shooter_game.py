#Игра Шутер!
import pygame
from pygame.locals import *
from random import randint
from time import time as timer

pygame.font.init()
font1 = pygame.font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 215, 0))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = pygame.font.Font(None, 36)


pygame.mixer.init()
pygame.mixer.music.load('space.ogg')
pygame.mixer.music.play()
fire = pygame.mixer.Sound('fire.ogg')


score = 0
max_score = 100
score_lost = 0
max_lost = 10
life = 3


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        pygame.sprite.Sprite.__init__(self)
        #super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        self.speed = player_speed   
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < width-80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, fluct):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.fluct = fluct
    def update(self):
        self.rect.y += self.speed
        global score_lost
        direction = randint(1, 2)
        if direction == 1:
            self.rect.x += self.fluct
        elif direction == 2:
            self.rect.x -= self.fluct
        # Исчезает если дойдет до края экрана
        if self.rect.y > height:
            self.rect.x = randint(80, width-80)
            self.rect.y = 0
            score_lost = score_lost + 1



width = 1000
height = 700

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Шутер!')
galaxy = pygame.transform.scale(pygame.image.load('galaxy.jpg'), (width, height))

player = Player('rocket.png', 5, height-100, 80, 100, 15)

ufos = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for i in range(1, 10):
    ufo = Enemy('ufo.png', randint(80, width-40), -40, 80, 50, randint(1, 10), randint(10, 30))
    ufos.add(ufo)

for i in range(1, 5):
    asteroid = Enemy('asteroid.png', randint(80, width-40), -40, 80, 50, randint(1, 5), 0)
    asteroids.add(asteroid)


FPS = 50

game_over = False
finish = False

rel_time = False
num_fire = 0

while not game_over:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game_over = True
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire += 1
                    fire.play()
                    player.fire()
                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if finish != True:
        window.blit(galaxy, (0, 0))

        player.update()
        ufos.update()
        bullets.update()
        asteroids.update()

        player.reset()
        ufos.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 2:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                rel_time = False    

        collides = pygame.sprite.groupcollide(ufos, bullets, True, True)
        for c in collides:
            score += 1
            ufo = Enemy('ufo.png', randint(80, width-80), -40, 80, 50, randint(1, 10), randint(10, 30))
            ufos.add(ufo)

        '''if pygame.sprite.spritecollide(player, ufos, False) or pygame.sprite.spritecollide(player, asteroids, False) or score_lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))'''

        if pygame.sprite.spritecollide(player, ufos, False) or pygame.sprite.spritecollide(player, asteroids, False):
            pygame.sprite.spritecollide(player, ufos, True)
            pygame.sprite.spritecollide(player, asteroids, True)
            life -= 1
        
        if life == 0 or score_lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= max_score:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено: ' + str(score_lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
        pygame.display.update()
        

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for u in ufos:
            u.kill()
        for a in asteroids:
            a.kill()

        pygame.time.delay(3000)
        for i in range(1, 6):
            ufo = Enemy('ufo.png', randint(80, width-40), -40, 80, 50, randint(1, 10), randint(10, 30))
            ufos.add(ufo)
        for i in range(1, 3):
            asteroid = Enemy('asteroid.png', randint(80, width-40), -40, 80, 50, randint(1, 5), 0)
            asteroids.add(asteroid)
        pygame.time.delay(50)
  
        
    pygame.time.delay(FPS)
