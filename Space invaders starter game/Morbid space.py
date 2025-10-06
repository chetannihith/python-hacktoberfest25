from random import randint
import pygame
from pygame.sprite import Sprite,GroupSingle,groupcollide
from pygame.locals import *
from sys import exit

pygame.init()

tamanho = 800, 600
fonte = pygame.font.SysFont('Chiller', 45)
fonte_perdeu = pygame.font.SysFont('Chiller', 60)
fonte_retornar = pygame.font.SysFont('Chiller', 50)

superficie = pygame.display.set_mode(size=(tamanho))
pygame.display.set_caption('Tie destroyer')
fundo = pygame.image.load(('C:/Users/Ricardo/Downloads/wallpapersden.com_galaxies-pixel-art_800x600.jpg'))
pygame.transform.scale(fundo, (tamanho))

class Spaceship(Sprite):
    def __init__(self, lasers):
        super().__init__()

        self.image = pygame.image.load('C:/Users/Ricardo/Downloads/NicePng_spaceship-sprite-png_3369998.png')
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        self.lasers = lasers
        self.velocidade = 3

    def tacar_laser(self):
        if len(self.lasers) < 15:
            self.lasers.add(Laser(*self.rect.center))

    def update(self):
        keys = pygame.key.get_pressed()

        laser_fonte = fonte.render(f'Bullets: {15 - len(self.lasers)}',True,(255, 255, 255))
        superficie.blit(laser_fonte, (20, 20))

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade

class Laser(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('C:/Users/Ricardo/Downloads/pngfind.com-bullet-bill-png-1931131.png')
        self.image = pygame.transform.scale(self.image,(22,17))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += 2

        if self.rect.x > tamanho[0]:
            self.kill()


class Tie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('C:/Users/Ricardo/Downloads/pngfind.com-tie-fighter-png-501552.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(800, randint(20, 580)))

    def update(self):
        global perdeu
        self.rect.x -= 0.1

        if self.rect.x == 0:
            self.kill()
            perdeu = True

grupo_Tie = pygame.sprite.Group()
grupo_Tie.add(Tie())
grupo_lasers = pygame.sprite.Group()
Nave = Spaceship(grupo_lasers)
grupo_nave = GroupSingle(Nave)

clock = pygame.time.Clock()
mortes = 0
round = 0
perdeu = False

while True:
    #clock.tick(400)

    if round % 120 == 0:
        if mortes < 20:
            grupo_Tie.add(Tie())
        for i in range(int(mortes / 20)):
            grupo_Tie.add(Tie())

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()
        if evento.type == KEYUP:
            if evento.key == K_SPACE:
                Nave.tacar_laser()
            if evento.key == K_ESCAPE:
                exit()
    if groupcollide(grupo_lasers, grupo_Tie, True, True):
        mortes += 1

    superficie.blit(fundo,(0,0))

    fonte_mortes = fonte.render(f'kills: {mortes}',True,(255, 255, 255))
    superficie.blit(fonte_mortes, (20, 70))

    grupo_nave.draw(superficie)
    grupo_Tie.draw(superficie)
    grupo_lasers.draw(superficie)
    grupo_nave.update()
    grupo_Tie.update()
    grupo_lasers.update()

    if perdeu:
        deu_F = fonte_perdeu.render('YOU DIED',True,(180, 0, 0))
        superficie.blit(deu_F, (280, 270))
        retorne = fonte_retornar.render('Digite ESC para sair e tente novamente!', True, (120,0,0))
        superficie.blit(retorne, (115, 320))

        pygame.display.update()
        pygame.time.delay(10)

    round += 1
    pygame.display.update()


