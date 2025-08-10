import pygame
import time
from Nave_Atira import nave, Maus, Tiro
from tela import Telas
from config import Altura, Largura, estado_jogo, larguracreini, Alturacreini

pygame.init()
tela = pygame.display.set_mode((Largura, Altura))
pygame.display.set_caption("Cauã Space Battle")

telas = Telas(tela)
clock = pygame.time.Clock()
nave_jogada = nave()
malvados = Maus()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        if evento.type == pygame.KEYDOWN:
            estado_jogo = telas.Alternar_telas(evento.key, estado_jogo)

    clock.tick(120)
    telas.Desenhar_Telas(estado_jogo)

    if estado_jogo == "jogando":
        pressionada = pygame.key.get_pressed()
        nave_jogada.movimentação(pressionada)
        nave_jogada.atirar()
        malvados.atualiza()

        nave_jogada.detectar_tiro(malvados.aliens)
        nave_jogada.detectar_coli(malvados.aliens)

        nave_jogada.Desenhar_nave(tela)

        for disparo in nave_jogada.tiros[:]:
            disparo.tiro_move()
            disparo.Desenhar_tiro(tela)

        for alien in malvados.aliens[:]:
            alien.queda()
            alien.desenho(tela)

        malvados.sai_tela()

    pygame.display.update()