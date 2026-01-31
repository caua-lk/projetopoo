import pygame
import time
import random
from const import Altura, Largura
from Tiros import Laser_boss, Tiro_Boss   

Size_Boss = (364, 364)

Boss_Image = pygame.image.load("Jogo/sprites/Boss_Image.png").convert_alpha()
Boss_Image = pygame.transform.scale(Boss_Image, Size_Boss)

Boss_Image_Charge = pygame.image.load("Jogo/sprites/Boss_Image_Charge.png").convert_alpha()
Boss_Image_Charge = pygame.transform.scale(Boss_Image_Charge, Size_Boss)

class Boss:
    def __init__(self):
        self.image = Boss_Image
        self.rect = self.image.get_rect()
        self.vida = 100
        self.velocidade = 2
        self.estado = "iniciando"
        self.tiros = []

        self.ult_ti = 0
        self.cadencia = 1.5
        self.rect.midtop = (Largura // 2,-Size_Boss[1])
        self.laser_duracao = 5 

        self.laser_fim = None
        self.laser_cooldown = 5

    def atualizar(self):
        if self.estado == "iniciando":
            self.rect.y += self.velocidade
            if self.rect.y >= 120:
                self.estado = "Atacar"

        elif self.estado == "Atacar":
            self.movimentar()
            self.atirar(shot=True)

            if (self.laser_fim is None or time.time() - self.laser_fim > self.laser_cooldown) and random.random() < 0.005:
                self.estado = "CarregandoLaser"
                self.image = Boss_Image_Charge
                self.laser_inicio = time.time()

        elif self.estado == "CarregandoLaser":

            if time.time() - self.laser_inicio > 7:
                self.estado = "Laser"
                self.tiros.append(Laser_boss(self)) 
                self.laser_inicio = time.time()

        elif self.estado == "Laser":
            if time.time() - self.laser_inicio > self.laser_duracao:
                self.estado = "Atacar"
                self.image = Boss_Image
                self.tiros = [tiro for tiro in self.tiros if not isinstance(tiro,Laser_boss)]
                self.laser_fim = time.time()
    def movimentar(self):
        self.rect.x += self.velocidade
        if self.rect.right >= (Largura - 40) or self.rect.left <= 10:
            self.velocidade *= -1

    def atirar(self, shot=False):
        tempo = time.time()
        if shot and (tempo - self.ult_ti > self.cadencia):
            direcoes = ["volatil1", "volatil2"]
            for direcao in direcoes:
                self.tiros.append(Tiro_Boss(self, direcao))
            self.ult_ti = tempo
