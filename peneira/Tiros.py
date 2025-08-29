import pygame
import time
from stat_game import estado_jogo
from const import Altura, Largura
import pygame.locals
pygame.init()
pygame.display.set_mode((Largura, Altura))
# --------------------------------------------------------------
# Otimização por meio de boas práticas ensinadas pela a IA
Tiro_nave = pygame.Surface((10, 20)).convert()
Tiro_nave.fill((255, 0, 0))


Tiro_sniper = pygame.Surface((6, 25)).convert()
Tiro_sniper.fill((255, 255, 0)) # Diferenciando cor


Tiro_alien = pygame.Surface((10, 20)).convert()
Tiro_alien.fill((0, 255, 0))
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


    def tiro_move(self):
        self.rect.y += self.velocidade
        if self.rect.top > Altura:
            self.kill()
    def desenhar_tiro(self, tela):
        tela.blit(self.imagem, self.rect)