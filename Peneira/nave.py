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

Penguim_image = pygame.image.load("sprites/NavePinguimDEF.png").convert_alpha()
Penguim_image = pygame.transform.scale(Penguim_image, SizeComom)

Ravage_image = pygame.image.load("sprites/NaveRavage.png").convert_alpha()
Ravage_image = pygame.transform.scale(Ravage_image, SizeComom)

Guns_Shot_image = pygame.image.load("sprites/NaveGunsShotDEF.png").convert_alpha()
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

        self.msg = ""
        self.msg_entTime = 0
        self.font = pygame.font.SysFont(None, 36)

        self.shield = False
        self.shield_endTime = 0

        self.no_damage = False
        self.no_damage_EndTime = 0
        self.max_life = 10
        self.max_damage = 6.5
    # Estrutura de encerramento universal das naves
    def morreu(self, explosions):
        explosions.append(Explosion(self.rect.center))
        estado_jogo.valor = "Gameover"
    # Verificação de colisão física com inimigos
    def detectar_coli(self, inimigos, explosions):
        for alien in inimigos[:]:
            if self.rect.colliderect(alien.rect):
                if self.shield:
                    explosions.append(Explosion(alien.rect.center))
                    inimigos.remove(alien)
                    continue
                if not self.no_damage:
                    self.vida -= 1
                    self.no_damage = True
                    self.no_damage_EndTime = time.time() + 2
                    inimigos.remove(alien) # Ao colidir o alien some
            if self.vida <= 0:
                self.morreu(explosions)

    # Verificação de colisão de tiros dos inimigos
    def detectar_tiro_alien(self, tiros_alien, explosions):
        for tiro in tiros_alien[:]:
            if self.rect.colliderect(tiro.rect):
                if self.shield or self.no_damage:
                    continue
                self.vida -= 1
                self.no_damage = True
                self.no_damage_EndTime = time.time() + 2
                tiros_alien.remove(tiro)
                if self.vida <= 0:
                    self.morreu(explosions)

    # Verificação de colisão de tiros contra os inimigos
    def detectar_tiro(self,inimigos, explosions, power_list):
        for tiro in self.tiros[:]:  # percorre uma cópia da lista
            for alien in inimigos[:]:
                if tiro.rect.colliderect(alien.rect):
                    alien.saude -= self.dano
                    if alien.saude <= 0:
                        self.points += alien.points
                        alien.morreu(explosions, power_list)
                        inimigos.remove(alien)
                    if tiro in self.tiros:
                        self.tiros.remove(tiro)
                    break 
    def detect_powerup(self,powerups):
        for p in powerups[:]:
            if self.rect.colliderect(p.rect):
                text = p.effect(self)
                self.msg = text
                self.msg_entTime = time.time() + 2
                powerups.remove(p)
    def desenhar_mensagem(self, tela):
        if self.msg and time.time() < self.msg_entTime:
            texto = self.font.render(self.msg, True, (255, 255, 0))
            tela.blit(texto, (Largura // 2 - texto.get_width() // 2, Altura - 80))

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
    def movimentação(self,mover_x = 0, mover_y = 0):
        self.rect.x += mover_x * self.velocidade
        self.rect.y += mover_y * self.velocidade
        self.limite()

    # Alternativas para tiros básicos
    def atirar(self, shot=False):
        tempo = time.time()
        if shot and (tempo - self.ult_ti > self.cadencia):
            self.tiros.append(Tiro(self, 'center'))
            self.ult_ti = tempo

    def Desenhar_nave(self, tela):
        if self.no_damage and time.time() < self.no_damage_EndTime:
            if int(time.time() * 10) % 2 == 0:
                tela.blit(self.imagem, self.rect)
        else:
                tela.blit(self.imagem, self.rect)
        
        if self.shield and time.time() < self.shield_endTime:
            pygame.draw.circle( tela , (0,255,255) , self.rect.center , max( self.rect.width , self.rect.height ) // 2 + 10 , 3)

                

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
    def atirar(self, shot):
        tempo = time.time()
        if shot and (tempo - self.ult_ti > self.cadencia):
            direcoes = ["center", "left", "right"]
            for direcao in direcoes:
                self.tiros.append(Tiro(self, direcao))
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
    def atirar(self,shot=False):
        tempo = time.time()
        if shot and (tempo - self.ult_ti > self.cadencia):
            self.tiros.append(TiroSniper(self))
            self.ult_ti = tempo

