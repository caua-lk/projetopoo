import pygame
import time
pygame.init()
class Explosion:
    def __init__(self, position):
        self.frames = [
            pygame.image.load(f"sprites/exp/explosion{i}.png").convert_alpha() 
            for i  in range(1,6) # para cada frame de explosão numerada
        ]
        self.index = 0
        self.pos = position
        self.timer = time.time()
        self.intervalo = 0.08
    def update(self):
        if time.time() - self.timer > self.intervalo:
            self.index += 1
            self.timer = time.time()
    def ended(self):
        return self.index >= len(self.frames)

    def draw(self, tela):
        if self.index < len(self.frames):
            imagem = pygame.transform.scale(self.frames[self.index], (94, 94))
            rect = imagem.get_rect(center=self.pos)
            tela.blit(imagem, rect)