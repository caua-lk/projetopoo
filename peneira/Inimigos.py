import pygame
import time
import random
from stat_game import estado_jogo
from const import Altura, Largura
from Tiros import GunAlien
from Explosion import Explosion
import pygame.locals
pygame.init()

# --------------------------------------------------------------
# Otimização por meio de boas práticas ensinadas pela a IA
SizeCommom = (96,96)
Death_Sound = pygame.mixer.Sound("Sounds/Explosion.wav")

Alien_simple_image = pygame.image.load("sprites/inimigo_simple.png").convert_alpha()
Alien_simple_image = pygame.transform.scale(Alien_simple_image, SizeCommom)
Alien_simple_image = pygame.transform.rotate(Alien_simple_image, 0)

Alien_seach_image = pygame.image.load("sprites/inimigo_seach.png").convert_alpha()
Alien_seach_image = pygame.transform.scale(Alien_seach_image, SizeCommom)
Alien_seach_image = pygame.transform.rotate(Alien_seach_image, 180)

Alien_gun_image = pygame.image.load("sprites/inimigo_gunner.png").convert_alpha()
Alien_gun_image = pygame.transform.scale(Alien_gun_image, SizeCommom)
Alien_gun_image = pygame.transform.rotate(Alien_gun_image, 180)

gun_sound = pygame.mixer.Sound("Sounds/Gun-Sound.wav")
# --------------------- Classe de Inimigos ---------------------
class Alien:

    def __init__(self, saude, points, velocidade=1):
        self.imagem = pygame.Surface((50, 50)) #testando
        self.imagem.fill((255,255,255))

        self.saude = saude
        self.points = points
        self.velocidade = velocidade

        self.rect = self.imagem.get_rect(midtop=(random.randint(50, Largura-50),0))
        self.lado = random.choice([-1,1])
        self.Death_sound = Death_Sound

    # Queda em zigzag para dificuldade 
    def queda(self):
        self.rect.y += self.velocidade
        self.rect.x += self.velocidade * self.lado
        if self.rect.left <= 0 or self.rect.right >= Largura:
            self.lado *= -1

    def desenho(self, tela):
        tela.blit(self.imagem, self.rect)
    def morreu(self, explosions):
        self.Death_sound.play()
        explosions.append(Explosion(self.rect.center))
# --------------------- Subclasse de Inimigos ---------------------

# Alien de início
class alien_simple(Alien):
    def __init__(self):

        # Fraco e frequente
        super().__init__(saude=6,points=10,velocidade=2)

        self.imagem = Alien_simple_image

        self.rect = self.imagem.get_rect(midtop=(random.randint(50, Largura - 50), 0))


# Busca a nave
class alien_seach(Alien):
    def __init__(self):

        # Irritante e perseguidor
        super().__init__(saude=12,points=25,velocidade=3)
        self.imagem = Alien_seach_image
        self.rect = self.imagem.get_rect(midtop=(random.randint(50, Largura - 50), 0))

    def seach_nave(self, nave):
        limit = Altura * 0.8
        # Verifica se o alien está acima da metade da tela
        # e a nave está abaixo dele
        if self.rect.centery < limit:
            # Persegue a nave
            direcao = pygame.math.Vector2(nave.rect.center) - pygame.math.Vector2(self.rect.center)
            if direcao.length() != 0:
                direcao = direcao.normalize()
            else:
                direcao = pygame.math.Vector2(0, 1)

            self.rect.x += direcao.x * (self.velocidade * 0.6)
            self.rect.y += direcao.y * self.velocidade
        else:
            # Se a nave estiver acima ou o alien passou do condicionado, desce reto
            self.rect.y += self.velocidade

# Inimigo que atira
class alien_gun(Alien):
    def __init__(self):
        super().__init__(saude=10,points=45,velocidade=2)
        self.Sound = gun_sound

        self.imagem = Alien_gun_image

        self.rect = self.imagem.get_rect(midtop=(random.randint(50, Largura - 50), 0))


        self.cadencia = 0.8
        self.tiros = []
        self.ult_ti = time.time()

    # Método para atirar de acordo com o período definido pela cadência
    def atirar(self, lista_global):
        tempo = time.time()
        if tempo - self.ult_ti > self.cadencia:
            novo_tiro = GunAlien(self)
            self.tiros.append(novo_tiro)
            lista_global.append(novo_tiro)
            self.Sound.play()
            self.ult_ti = tempo

class Maus:
    def __init__(self):
        self.aliens = [] 
        self.ult_spawn = time.time()
        self.tempo_ini = time.time()
        self.intervalo = 3
        self.spawners = 1
    def atualiza(self):
        tempo_agora = time.time()
        tempo_jogo = tempo_agora - self.tempo_ini

        self.spawners = min(1 + (int(tempo_jogo/45)), 2)
        self.intervalo = max(1.5, self.intervalo * 0.85)

        # Opções disponíveis para inimigos
        op_aliens = [alien_simple, alien_seach, alien_gun] 

        # Estrutura de progressão de dificuldade
        valia = [
            max(0.7 - tempo_jogo * 0.0001, 0.3),  # alien_simple
            min(0.2 + tempo_jogo * 0.0002, 0.4),  # alien_seach
            min(0.1 + tempo_jogo * 0.0001, 0.3)   # alien_gun
        ]
        if tempo_agora - self.ult_spawn > self.intervalo:
            for t in range(self.spawners):
                escolha_alien = random.choices(op_aliens, weights=valia)[0]
                self.aliens.append(escolha_alien())
            self.ult_spawn = tempo_agora
            
    def sai_tela(self):
        self.aliens = [alien for alien in self.aliens if alien.rect.top <= Altura]