import pygame
import time
import serial
from tela import Telas
from config import reiniciar_jogo, criar_nave_escolhida
from const import Altura, Largura
from stat_game import estado_jogo
from Inimigos import Maus, alien_gun, alien_seach, alien_simple
from entrada import view_commands

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
pygame.joystick.init()
tela = pygame.display.set_mode((Largura, Altura))

icon = pygame.image.load('sprites/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Blitz Stars")

joystick = pygame.joystick.Joystick(0) if pygame.joystick.get_count() > 0 else None
if joystick:
    joystick.init()
try:
    arduino = serial.Serial("COM3", 9600) # Ajustar de acordo com entrada USB
except:
    arduino = None
    
estado_jogo.nave_escolhida = {"Nome": "Penguim"}
estado_jogo.Tocar_musica()
nave_jogada, malvados = reiniciar_jogo()

tiros_dos_aliens = []
explosions = []
power_list = []
telas = Telas(tela)
clock = pygame.time.Clock()
# Função para reiniciar o jogo (usada ao voltar para o menu)
# Loop principal do jogo
while True:
    for evento in pygame.event.get():  # Captura eventos do teclado e mouse
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for botao in telas.buttons.get(estado_jogo.valor, []):
                if botao.rect.collidepoint(evento.pos):
                    if botao.text == "Confirmar Escolha" and telas.nave_selecionada:
                        nave_jogada, malvados = botao.callback(estado_jogo)
                    else:
                        botao.callback(estado_jogo) # Executa a ação do botão clicado
    comands = view_commands(joystick, arduino)
    estado_jogo, new, enemy = telas.Alternar_telas(comands, estado_jogo, nave_jogada)
    if estado_jogo.valor == "selecao":
        if comands["Next"]:
            telas.roll_nave(+1, estado_jogo)
        if comands["Before"]:
            telas.roll_nave(-1, estado_jogo)
    if new:
        nave_jogada = new
    if enemy:
        malvados = enemy
    clock.tick(60)  # Limita o jogo a 60 FPS
    telas.Desenhar_Telas(estado_jogo,nave_jogada)  # Desenha a tela atual (seleção, início, etc.)
    if estado_jogo.valor in ["inicio", "Gameover"]:
        tiros_dos_aliens.clear()
        explosions.clear()
        nave_jogada.tiros.clear()
    # Se estiver no menu e a nave estiver "morta", reinicia o jogo
    if estado_jogo.valor == "inicio" and nave_jogada.vida <= 0:
        nave_jogada, malvados = reiniciar_jogo()

    # Lógica principal do jogo
    if estado_jogo.valor == "jogando":

        nave_jogada.movimentação(comands["mover_x"], comands["mover_y"])  # Move a nave com base nas teclas pressionadas
        nave_jogada.atirar(comands["shot_button"])  # Verifica se a nave deve atirar

        malvados.atualiza()  # Atualiza posição e estado dos inimigos

        nave_jogada.detectar_tiro(malvados.aliens, explosions, power_list)  # Verifica se a nave foi atingida
        nave_jogada.detectar_coli(malvados.aliens, explosions)  # Verifica colisões com inimigos
        nave_jogada.detect_powerup(power_list)

        if nave_jogada.shield and time.time() > nave_jogada.shield_endTime:
            nave_jogada.shield = False

        if nave_jogada.no_damage and time.time() > nave_jogada.no_damage_EndTime:
            nave_jogada.no_damage = False

        # Atualiza e desenha cada inimigo
        for alien in malvados.aliens[:]:
            if isinstance(alien, alien_seach): # Alien que vem do alien_seach
                alien.seach_nave(nave_jogada)  # Inimigo especial persegue a nave
            else:
                alien.queda()  # Movimento padrão
            alien.desenho(tela)

            if hasattr(alien, "atirar"): # Alien que houver o método atirar
                alien.atirar(tiros_dos_aliens)  # Inimigo dispara tiros
        for powerup in power_list[:]:
            powerup.update()
            powerup.draw(tela)
            if powerup.rect.top > Altura:
                power_list.remove(powerup)
        # Atualiza e desenha os tiros dos inimigos
        for tiro in tiros_dos_aliens[:]:
            tiro.tiro_move()
            if tiro.rect.top > Altura:
                tiros_dos_aliens.remove(tiro)  # Remove tiro fora da tela
            else:
                tiro.desenhar_tiro(tela)

        nave_jogada.detectar_tiro_alien(tiros_dos_aliens, explosions)  # Verifica se a nave foi atingida por tiro inimigo
        for disparo in nave_jogada.tiros[:]:
            for alien in malvados.aliens[:]:
                if disparo.rect.colliderect(alien.rect):
                    alien.saude -= nave_jogada.dano
                    if alien.saude <= 0:
                        nave_jogada.points += alien.points
                        alien.morreu(explosions, power_list)
                        malvados.aliens.remove(alien)
                    if disparo in nave_jogada.tiros:
                        nave_jogada.tiros.remove(disparo)
                    break
        if nave_jogada.vida <= 0:
            telas.randomize_gameover()
            estado_jogo.valor = "Gameover"
            continue  # Pula o restante do loop para mostrar tela de fim de jogo

        nave_jogada.Desenhar_nave(tela)  # Desenha a nave do jogador
        nave_jogada.desenhar_mensagem(tela)
        # Atualiza e desenha os tiros da nave
        for disparo in nave_jogada.tiros[:]:
            disparo.tiro_move()
            disparo.Desenhar_tiro(tela)

        malvados.sai_tela()  # Remove inimigos que saíram da tela
        for explosao in explosions[:]: # Explosão
            explosao.update()
            explosao.draw(tela)
            if explosao.ended():
                explosions.remove(explosao)
    pygame.display.update()  # Atualiza a tela com tudo que foi desenhado