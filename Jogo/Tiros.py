import pygame
import time
from stat_game import estado_jogo
from const import Altura, Largura
import pygame.locals
pygame.init()
pygame.display.set_mode((Largura, Altura))
# --------------------------------------------------------------
# Otimização por meio de boas práticas ensinadas pela a IA
Tiro_nave = pygame.image.load("Jogo/sprites/Bullet_commom.png").convert_alpha()
Tiro_nave = pygame.transform.scale(Tiro_nave, (30, 25))

Tiro_sniper = pygame.image.load("Jogo/sprites/Impact_bullet.png").convert_alpha()
Tiro_sniper = pygame.transform.scale(Tiro_sniper,(10, 30))

Tiro_alien = pygame.image.load("Jogo/sprites/Bullet_Alien.png")
Tiro_alien = pygame.transform.scale(Tiro_alien, (30, 25))

Tiro_boss = pygame.image.load("Jogo/sprites/Bullet_Alien.png")
Tiro_boss = pygame.transform.scale(Tiro_alien, (60, 50))

Tiro_sound = pygame.mixer.Sound("Jogo/Sounds/Gun-Sound.wav")
Tiro_sound.set_volume(1.0)

Laser_1 = pygame.image.load("Jogo/sprites/Lasers/Laser_1.png").convert_alpha()
Laser_1 = pygame.transform.scale(Laser_1, (Largura // 2 - 20, Altura))

Laser_2 = pygame.image.load("Jogo/sprites/Lasers/Laser_2.png").convert_alpha()
Laser_2 = pygame.transform.scale(Laser_2, (Largura // 2 - 20, Altura))

Laser_3 = pygame.image.load("Jogo/sprites/Lasers/Laser_3.png").convert_alpha()
Laser_3 = pygame.transform.scale(Laser_3, (Largura // 2 - 20, Altura))

# --------------------- Classe de Tiros ---------------------
class Tiro(pygame.sprite.Sprite):
    def __init__(self, nave, direcao = "center"):
        super().__init__()
        self.nave = nave 

        self.imagem = Tiro_nave

        self.velocidade_y = 4
        self.velocidade_x = 0


        # Direcionamento do tiro de acordo com direção induzida pelo comando de nave
        if direcao == "center":
            self.rect = self.imagem.get_rect(midbottom=nave.rect.midtop)
        elif direcao == "left":
            self.rect = self.imagem.get_rect(midbottom=(nave.rect.left, nave.rect.centery))
            self.velocidade_x = -2
        elif direcao == "right":
            self.rect = self.imagem.get_rect(midbottom=(nave.rect.right, nave.rect.centery))
            self.velocidade_x = 2

        self.sound = Tiro_sound
        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(self.sound)

    def tiro_move(self):
        self.rect.y -= self.velocidade_y
        self.rect.x += self.velocidade_x * 2.5

        # Retirando tiros passados com sprite.Sprite
        if (self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > Largura):
                self.kill() 

    # Desenhando tiros
    def Desenhar_tiro(self, tela):
        tela.blit(self.imagem, self.rect)

# Classe de tiros para nave sniper
class TiroSniper(pygame.sprite.Sprite):
    def __init__(self,nave):
        super().__init__()
        self.nave = nave

        self.imagem = Tiro_sniper

        self.rect = self.imagem.get_rect(midbottom=nave.rect.midtop)
        self.velocidade_y = 10  # Velocidade maior

        self.sound = Tiro_sound
        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(self.sound)

    def tiro_move(self):
        self.rect.y -= self.velocidade_y
        if self.rect.bottom < 0:
            self.kill()

    def Desenhar_tiro(self, tela):
        tela.blit(self.imagem, self.rect)
class Tiro_Laser(pygame.sprite.Sprite):
    def __init__(self, nave):
        super().__init__()
        self.nave = nave

#        self.imagem = tirolaser
        self.rect = self.get_rect()
# Tiro dos inimigos
class GunAlien(pygame.sprite.Sprite):
    def __init__(self, alien):
        super().__init__()
        self.alien = alien

        self.imagem = Tiro_alien

        self.rect = self.imagem.get_rect(midtop=alien.rect.midbottom)
        self.velocidade = 4
        
        self.sound = Tiro_sound
        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(self.sound)

    def tiro_move(self):
        self.rect.y += self.velocidade
        if self.rect.top > Altura:
            self.kill()
    def desenhar_tiro(self, tela):
        tela.blit(self.imagem, self.rect)

class Tiro_Boss(pygame.sprite.Sprite):
    def __init__(self, boss, direcao="volatil1"):
        super().__init__()
        self.boss = boss
        self.imagem = Tiro_boss  

        boss_x, boss_y = boss.rect.midbottom
        self.rect = self.imagem.get_rect(midtop=(boss_x , boss_y - 30))

        self.velocidade_y = 5

        if direcao == "volatil1":
            self.velocidade_x = -2
        elif direcao == "volatil2":
            self.velocidade_x = 2
        else:
            self.velocidade_x = 0

        # Som do tiro
        self.sound = Tiro_sound
        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(self.sound)

    def tiro_move(self):
        # Movimento do tiro
        self.rect.y += self.velocidade_y
        self.rect.x += self.velocidade_x

        if self.rect.top > Altura or self.rect.right < 0 or self.rect.left > Largura:
            self.kill()

    def desenhar_tiro(self, tela):
        tela.blit(self.imagem, self.rect)
class Laser_boss(pygame.sprite.Sprite):
    def __init__(self, boss):
        super().__init__()
        self.boss = boss

        # Carrega os sprites do laser aqui
        self.sprites = [Laser_1,Laser_2,Laser_3]

        self.frame_index = 0
        self.image = self.sprites[self.frame_index]
        boss_x, boss_y = boss.rect.midbottom
        self.rect = self.image.get_rect(midtop=(boss_x , boss_y - 40))

        self.last_update = time.time()
        self.frame_rate = 0.2

    def tiro_move(self):
        now = time.time()
        if now - self.last_update > self.frame_rate:
            self.frame_index = (self.frame_index + 1) % len(self.sprites)
            self.image = self.sprites[self.frame_index]
            self.last_update = now

    def desenhar_tiro(self, tela):
        tela.blit(self.image, self.rect)
