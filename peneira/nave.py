import pygame
import time
from stat_game import estado_jogo
from const import Altura, Largura
from Tiros import Tiro, TiroSniper
from Explosion import Explosion
import pygame.locals
pygame.init()

# --------------------------------------------------------------
# Otimização por meio de boas práticas ensinadas pela a IA
SizeComom = (96,96)
Gun_Sound =  pygame.mixer.Sound("Sounds/Gun-Sound.wav")
explosion = pygame.mixer.Sound("Sounds/Explosion.wav")

Penguim_image = pygame.image.load("sprites/NavePinguim.png").convert_alpha()
Penguim_image = pygame.transform.scale(Penguim_image, SizeComom)

Ravage_image = pygame.image.load("sprites/NaveRavage.png").convert_alpha()
Ravage_image = pygame.transform.scale(Ravage_image, SizeComom)

Guns_Shot_image = pygame.image.load("sprites/NaveGunsShot.png").convert_alpha()
Guns_Shot_image = pygame.transform.scale(Guns_Shot_image, SizeComom)

Tank_image = pygame.image.load("sprites/NaveWar.png").convert_alpha()
Tank_image = pygame.transform.scale(Tank_image, SizeComom)

Sniper_image = pygame.image.load("sprites/NaveSniper.png").convert_alpha()
Sniper_image = pygame.transform.scale(Sniper_image, SizeComom)
# --------------------- Classe de Naves ---------------------

class navebase:
    def __init__(self, velocidade, vida, dano,cadencia):

        # Preenche com uma cor padrão (Caso a imagem não carregue)
        self.imagem = pygame.Surface(SizeComom)
        self.imagem = pygame.transform.scale(self.imagem, SizeComom)

        # Define onde a nave começará
        self.rect = self.imagem.get_rect(midbottom=(Largura//2,Altura-50))
        self.velocidade = velocidade
        self.vida = vida
        self.tiros = []
        self.dano = dano
        self.ult_ti = time.time()
        self.cadencia = cadencia
        self.powerup = [] # Lista para upgrades
        self.points = 0
        self.Sound = Gun_Sound
        self.Death_sound = explosion

    # Estrutura de encerramento universal das naves
    def morreu(self, explosions):
        self.Death_sound.play()
        explosions.append(Explosion(self.rect.center))
        estado_jogo.valor = "Gameover"
    # Verificação de colisão física com inimigos
    def detectar_coli(self, inimigos, explosions):
        for alien in inimigos[:]:
            if self.rect.colliderect(alien.rect):
                self.vida -= 1
                inimigos.remove(alien) # Ao colidir o alien some
            if self.vida <= 0:
                self.morreu(explosions)

    # Verificação de colisão de tiros dos inimigos
    def detectar_tiro_alien(self, tiros_alien, explosions):
        for tiro in tiros_alien[:]:
            if self.rect.colliderect(tiro.rect):
                self.vida -= 1
                tiros_alien.remove(tiro)
                if self.vida <= 0:
                    self.morreu(explosions)

    # Verificação de colisão de tiros contra os inimigos
    def detectar_tiro(self,inimigos, explosions):
        for tiro in self.tiros[:]:  # percorre uma cópia da lista
            for alien in inimigos[:]:
                if tiro.rect.colliderect(alien.rect):
                    alien.saude -= self.dano
                    if alien.saude <= 0:
                        self.points += alien.points
                        alien.morreu(explosions)
                        inimigos.remove(alien)
                    if tiro in self.tiros:
                        self.tiros.remove(tiro)
                    break 

    # Define capacidade de movimento
    def limite(self):

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Largura:
            self.rect.right = Largura
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Altura:
            self.rect.bottom = Altura

    # Controle do jogador
    def movimentação(self, pressionada):
        if pressionada[pygame.K_a]:
            self.rect.x -= self.velocidade
        if pressionada[pygame.K_d]:
            self.rect.x += self.velocidade
        if pressionada[pygame.K_w]:
            self.rect.y -= self.velocidade
        if pressionada[pygame.K_s]:
            self.rect.y += self.velocidade
        self.limite()

    # Alternativas para tiros básicos
    def atirar(self):
        pressionada = pygame.key.get_pressed() 
        tempo = time.time()
        if tempo - self.ult_ti > self.cadencia:
            if pressionada[pygame.K_UP]: 
                self.tiros.append(Tiro(self, 'center'))
                self.Sound.play()
                self.ult_ti = tempo

    def Desenhar_nave(self, tela):
        tela.blit(self.imagem, self.rect)

# --------------------- Subclasse de Naves ---------------------

# Nave equilibrada
class NavePenguim(navebase):
    def __init__(self):
        super().__init__(velocidade=5,vida=6,dano=2.5,cadencia=0.45)

        self.imagem = Penguim_image
        self.rect = self.imagem.get_rect(midbottom=(Largura // 2, Altura - 50))

# Nave rápida e ofensiva
class NaveAtaque(navebase):
    def __init__(self):
        super().__init__(velocidade=6,vida=5,dano=3.5,cadencia=0.4)

        self.imagem = Ravage_image
        self.rect = self.imagem.get_rect(midbottom=(Largura // 2, Altura - 50))

# Nave de rajada, mas com pouco dano
class Nave_Guns_Shot(navebase):
    def __init__(self):
        super().__init__(velocidade=4,vida=5,dano=1.2,cadencia=0.25)

        self.imagem = Guns_Shot_image
        self.rect = self.imagem.get_rect(midbottom=(Largura // 2, Altura - 50))
# Alternativas de tiro para nave de rajada
    def atirar(self):
        pressionada = pygame.key.get_pressed()
        tempo = time.time()
        if tempo - self.ult_ti > self.cadencia:
            direcoes = []
            if pressionada[pygame.K_UP]:
                direcoes.append("center")
            if pressionada[pygame.K_LEFT]:
                direcoes.append("left")
            if pressionada[pygame.K_RIGHT]:
                direcoes.append("right")
            for direcao in direcoes:
                self.tiros.append(Tiro(self, direcao))
            if direcoes:
                self.Sound.play()
                self.ult_ti = tempo
# Nave resistente e constante
class Nave_tank(navebase):
    def __init__(self):
        super().__init__(velocidade=3, vida=9, dano=2.2, cadencia=0.6)

        self.imagem = Tank_image
        self.rect = self.imagem.get_rect(midbottom=(Largura // 2, Altura - 50))

# Nave com precisão e letalidade alta
class Nave_sniper(navebase):
    def __init__(self):
        super().__init__(velocidade=4, vida=5, dano=6, cadencia=1.2)

        self.imagem = Sniper_image
        self.rect = self.imagem.get_rect(midbottom=(Largura // 2, Altura - 50))

    # Estrutura própria de tiro para tiro preciso e letal
    def atirar(self):
        tempo = time.time()
        pressionada = pygame.key.get_pressed()
        if tempo - self.ult_ti > self.cadencia and pressionada:
            if pressionada[pygame.K_UP]:
                self.tiros.append(TiroSniper(self))
                self.Sound.play()
                self.ult_ti = tempo
# Powerups futuros
class Powerup:
    def __init__(self, image):
        self.image = image
    def draw(self):
        pygame.blit(self.image, (64,64))
    def effect(self,nave):
        pass
