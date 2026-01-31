import pygame
import time
import serial
from tela import Telas
from config import reiniciar_jogo
from const import Altura, Largura
from stat_game import estado_jogo
from Inimigos import Maus, alien_gun, alien_seach, alien_simple
from entrada import view_commands, controller_map, detect
from boss import Boss
from Tiros import Laser_boss

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
pygame.joystick.init()

tela = pygame.display.set_mode((Largura, Altura))
icon = pygame.image.load('Jogo/sprites/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Blitz Stars")

# Inicializa joystick
joystick = None
map = controller_map['Generic']
if pygame.joystick.get_count() > 0:
    try:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        tipe = detect(joystick)
        map = controller_map[tipe]
    except:
        joystick = None

# Inicializa Arduino
arduino = None
try:
    arduino = serial.Serial("COM3", 9600, timeout=0.01)
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

boss = None
Boss_Show = 2000

# Loop principal
while True:
    # Reconexão joystick/arduino
    if joystick is None and pygame.joystick.get_count() > 0:
        try:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            tipe = detect(joystick)
            map = controller_map[tipe]
        except:
            joystick = None
            map = controller_map['Generic']
    if arduino is None:
        try:
            arduino = serial.Serial("COM3", 9600, timeout=0.01)
        except:
            arduino = None

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for botao in telas.buttons.get(estado_jogo.valor, []):
                if botao.rect.collidepoint(evento.pos):
                    if botao.text == "Confirmar Escolha" and telas.nave_selecionada:
                        nave_jogada, malvados = botao.callback(estado_jogo)
                    else:
                        botao.callback(estado_jogo)

    # Comandos
    try:
        comands = view_commands(joystick, arduino, map)
    except:
        joystick = None
        arduino = None
        comands = view_commands(None, None, controller_map['Generic'])

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

    clock.tick(60)
    telas.Desenhar_Telas(estado_jogo, nave_jogada)

    # Gameplay
    if estado_jogo.valor in ("jogando", "Boss"):
        nave_jogada.movimentação(comands["mover_x"], comands["mover_y"])
        nave_jogada.atirar(comands["shot_button"])

        # Atualiza inimigos só se não houver boss
        if boss is None:
            malvados.atualiza()

        nave_jogada.detectar_tiro(malvados.aliens, explosions, power_list)
        nave_jogada.detectar_coli(malvados.aliens, explosions)
        nave_jogada.detect_powerup(power_list)

        # Spawn boss
        if nave_jogada.points >= Boss_Show and boss is None:
            boss = Boss()
            estado_jogo.valor = "Boss"
            malvados.aliens.clear()
            tiros_dos_aliens.clear()

        # Boss ativo
        if boss:
            boss.atualizar()
            tela.blit(boss.image, boss.rect)

            for tiro in boss.tiros[:]:
                tiro.tiro_move()
                tiro.desenhar_tiro(tela)
                if tiro.rect.colliderect(nave_jogada.rect) and not nave_jogada.no_damage:
                    if isinstance(tiro, Laser_boss):
                        nave_jogada.vida -= 1
                    else:
                        nave_jogada.vida -= 2
                        boss.tiros.remove(tiro)
                    nave_jogada.no_damage = True
                    nave_jogada.no_damage_EndTime = time.time() + 2

            for disparo in nave_jogada.tiros[:]:
                if disparo.rect.colliderect(boss.rect):
                    boss.vida -= nave_jogada.dano
                    nave_jogada.tiros.remove(disparo)
                    if boss.vida <= 0:
                        boss = None
                        Boss_Show *= 2
                        estado_jogo.valor = "jogando"

        # Inimigos normais só se não houver boss
        if boss is None:
            for alien in malvados.aliens[:]:
                if isinstance(alien, alien_seach):
                    alien.seach_nave(nave_jogada)
                else:
                    alien.queda()
                alien.desenho(tela)
                if hasattr(alien, "atirar"):
                    alien.atirar(tiros_dos_aliens)

        # Powerups
        for powerup in power_list[:]:
            powerup.update()
            powerup.draw(tela)
            if powerup.rect.top > Altura:
                power_list.remove(powerup)

        # Tiros inimigos só se não houver boss
        if boss is None:
            for tiro in tiros_dos_aliens[:]:
                tiro.tiro_move()
                if tiro.rect.top > Altura:
                    tiros_dos_aliens.remove(tiro)
                else:
                    tiro.desenhar_tiro(tela)

        # Dano da nave nos inimigos
        if boss is None:
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

        # Escudo/invencibilidade
        if nave_jogada.shield and time.time() > nave_jogada.shield_endTime:
            nave_jogada.shield = False
        if nave_jogada.no_damage and time.time() > nave_jogada.no_damage_EndTime:
            nave_jogada.no_damage = False

        # Game over
        if nave_jogada.vida <= 0:
            telas.randomize_gameover()
            estado_jogo.valor = "Gameover"
            continue

        # Nave e HUD
        nave_jogada.Desenhar_nave(tela)
        nave_jogada.desenhar_mensagem(tela)

        # Tiros da nave
        for disparo in nave_jogada.tiros[:]:
            disparo.tiro_move()
            disparo.Desenhar_tiro(tela)

        # Limpeza inimigos fora da tela
        if boss is None:
            malvados.sai_tela()

        # Explosões
        for explosao in explosions[:]:
            explosao.update()
            explosao.draw(tela)
            if explosao.ended():
                explosions.remove(explosao)

    # Mouse visível
    if estado_jogo.valor in ("jogando", "Boss"):
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)

    # Atualiza tela
    pygame.display.update()
