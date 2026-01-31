import pygame
import time
pygame.init()
# --------------------------------------------------------------
# Otimização por meio de boas práticas ensinadas pela a IA
commom_size = (32,32)
sort_image = pygame.image.load("Jogo/sprites/itemSort.png").convert_alpha()
sort_image = pygame.transform.scale(sort_image,commom_size)
# --------------------------------------------------------------
class Powerup:
    def __init__(self,pos):
        self.image = sort_image
        self.rect = self.image.get_rect(center=pos)
        self.speed = 2
    def update(self):
        self.rect.y += self.speed
    def draw(self,tela):
        tela.blit(self.image, self.rect)
    def effect(self):
        pass

class Powerup_Life(Powerup):
    def __init__(self, pos):
        super().__init__(pos)
    def effect(self, nave):
        if nave.vida < nave.max_life:
            nave.vida += 1
            return "Power-up: Vida +1"
        return "Vidá já está no máximo"
class Powerup_Damage(Powerup):
    def __init__(self, pos):
        super().__init__(pos)
    def effect(self,nave):
        if nave.dano < nave.max_damage:
            nave.dano += 0.5
            return "Power-up: Dano +0.5"
        return "Dano já está no máximo"
class Powerup_Shield(Powerup):
    def __init__(self, pos):
        super().__init__(pos)
    def effect(self,nave):
        nave.shield = True
        nave.shield_endTime = time.time() + 5
        return "Power-up: Escudo ativado"
