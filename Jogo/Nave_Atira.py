import pygame
import time
import random
from config import Altura , Largura, estado_jogo
import pygame.locals
pygame.init()
class nave:

    def __init__(self):
        self.imagem = pygame.Surface((50, 50)) #testando
        self.imagem.fill((0, 255, 255))

        self.rect = self.imagem.get_rect(midbottom=(Largura//2,Altura-50))
        self.velocidade = 4
        self.vida = 3
        self.tiros = []
        self.dano = 1
        self.ult_ti = time.time()
        self.cadencia = 0.2
        self.powerup = None

    def detectar_coli(self,inimigos):
        for alien in inimigos[:]:
            if self.rect.colliderect(alien.rect):
                self.vida -=1
                inimigos.remove(alien) # Se toma dano some alien
            if self.vida <= 0:
                estado_jogo == "inicio"
    def detectar_tiro(self,inimigo):
        for tiro in self.tiros[:]:
            for alien in inimigo[:]:
                if tiro.rect.colliderect(alien.rect):
                    alien.saude -= self.dano
                    self.tiros.remove(tiro)
                    if alien.saude <= 0:
                        inimigo.remove(alien)

    def limite(self): # Não sai da tela

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Largura:
            self.rect.right = Largura
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Altura:
            self.rect.bottom = Altura

    def movimentação(self, pressionada):
        # Controle do jogador
        if pressionada[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if pressionada[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if pressionada[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if pressionada[pygame.K_DOWN]:
            self.rect.y += self.velocidade
        self.limite()
    def atirar(self):
        pressionada = pygame.key.get_pressed() 
        tempo = time.time()
        if pressionada[pygame.K_SPACE] and (tempo - self.ult_ti > self.cadencia): 
            self.tiros.append(Tiro(self))
            self.ult_ti = tempo # garante a atualização dos tiros do usuárioo
    def Desenhar_nave(self, tela):
        tela.blit(self.imagem, self.rect)
class Powerups:
    def __init__(self, efeito,imagem,):
        self.efeito = efeito
        self.imagem = pygame.Surface((50, 50)) #testando
        self.imagem.fill((100,100,100))
class power_dano(Powerups):
    def __init__(self):
        super().__init__("dano", pygame.Surface((50, 50)))
        self.imagem.fill((150, 0, 150))

class Tiro:
    def __init__(self, nave):
        self.nave = nave 
        self.imagem = pygame.Surface((10, 20))
        self.imagem.fill((255, 0, 0))
        self.rect = self.imagem.get_rect(midbottom=nave.rect.midtop)
        self.velocidade = 4

    def tiro_move(self):
        self.rect.y -= self.velocidade


        if self.rect.bottom < 0:
            if self in self.nave.tiros:
                self.nave.tiros.remove(self)

    def Desenhar_tiro(self, tela):
        tela.blit(self.imagem, self.rect)

class Alien:

    def __init__(self, cor, saude, pontos, velocidade=1):
        self.imagem = pygame.Surface((50, 50)) #testando
        self.cor = cor
        self.imagem.fill((self.cor))
        self.saude = saude
        self.pontos = pontos
        self.velocidade = velocidade
        self.rect = self.imagem.get_rect(midtop=(random.randint(50, Largura-50),0))
        self.lado = random.choice([-1,1])
    def queda(self):
        self.rect.y += self.velocidade
        self.rect.x += self.velocidade * self.lado
        if self.rect.left <= 0 or self.rect.right >= Largura:
            self.lado *= -1

    def desenho(self, tela):
        tela.blit(self.imagem, self.rect)

class ali_fraco(Alien):
    def __init__(self):
        super().__init__((255, 0, 0),2, 2) # vemelho

class ali_resis(Alien):
    def __init__(self):
        super().__init__((0, 255, 0),4, 5) #verde

class minichefe(Alien):
    def __init__(self):
        super().__init__((255, 255, 0), 7, 20)#amarelo
class Maus:
    def __init__(self):
        self.aliens = [] 
        self.ult_spawn = time.time()
        self.tempo_ini = time.time()
        self.intervalo = 1
        self.spawners = 1
    def atualiza(self):
        tempo_agora = time.time()
        tempo_jogo = tempo_agora - self.tempo_ini

        self.intervalo = max(1, self.intervalo * 0.995)
        self.spawners = min(1 + (int(tempo_jogo/30)), 4)
        op_aliens = [ali_fraco, ali_resis, minichefe]
        valia = [
            max(0.8 - tempo_jogo * 0.001, 0.6),  
            min(0.1 + tempo_jogo * 0.0002, 0.25),  
            min(0.05 + tempo_jogo * 0.00001, 0.1)  
        ]
        if tempo_agora - self.ult_spawn > self.intervalo:
            for t in range(self.spawners):
                escolha_alien = random.choices(op_aliens, weights=valia)[0]
                self.aliens.append(escolha_alien())
            self.ult_spawn = tempo_agora
    def sai_tela(self):
        for alien in self.aliens[:]:
            if alien.rect.top > Altura:
                self.aliens.remove(alien)