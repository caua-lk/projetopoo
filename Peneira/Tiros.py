import pygame
import time
from stat_game import estado_jogo
from const import Altura, Largura
import pygame.locals
pygame.init()
pygame.display.set_mode((Largura, Altura))
# --------------------------------------------------------------
# Otimização por meio de boas práticas ensinadas pela a IA
Tiro_nave = pygame.image.load("sprites/Bullet_commom.png").convert_alpha()
Tiro_nave = pygame.transform.scale(Tiro_nave, (30, 25))

Tiro_sniper = pygame.image.load("sprites/Impact_bullet.png").convert_alpha()
Tiro_sniper = pygame.transform.scale(Tiro_sniper,(10, 30))

Tiro_alien = pygame.image.load("sprites/Bullet_Alien.png")
Tiro_alien = pygame.transform.scale(Tiro_alien, (30, 25))

Tiro_sound = pygame.mixer.Sound("Sounds/Gun-Sound.wav")
Tiro_sound.set_volume(1.0)
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