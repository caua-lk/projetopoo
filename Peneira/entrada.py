import pygame
import serial
import time

pygame.init()
pygame.joystick.init()

cooldowns = {
    "Next": 0,
    "Before": 0,
    "Enter": 0
}
cooldown_delay = 0.3  # segundos

def view_commands(joystick=None, arduino=None):
    comands = {
        "mover_x": 0,
        "mover_y": 0,
        "shot_button": False,
        "Next": False,
        "Before": False,
        "Enter": False,
    }

    # Teclado
    pressionada = pygame.key.get_pressed()
    if pressionada:
        if pressionada[pygame.K_a]:
            comands["mover_x"] -= 1
        if pressionada[pygame.K_d]:
            comands["mover_x"] += 1
        if pressionada[pygame.K_w]:
            comands["mover_y"] -= 1
        if pressionada[pygame.K_s]:
            comands["mover_y"] += 1
        if pressionada[pygame.K_UP]:
            comands["shot_button"] = True
        if pressionada[pygame.K_ESCAPE] or pressionada[pygame.K_LEFT]:
            comands["Before"] = True
        if pressionada[pygame.K_RIGHT]:
            comands["Next"] = True
        if pressionada[pygame.K_RETURN]:
            comands["Enter"] = True

    # Controle USB
    if joystick:
        eixo_x = joystick.get_axis(2)
        eixo_y = joystick.get_axis(3)
        if abs(eixo_x) > 0.2:
            comands["mover_x"] += round(eixo_x)
        if abs(eixo_y) > 0.2:
            comands["mover_y"] += round(eixo_y)
        if joystick.get_button(0):  # Botão A
            comands["shot_button"] = True
        if joystick.get_button(1):
            comands["Next"] = True
        if joystick.get_button(2):
            comands["Before"] = True
        if joystick.get_button(3):
            comands["Enter"] = True

    # Arduino
    if arduino and arduino.readable():
        try:
            linha = arduino.readline().decode().strip()
            valores = linha.split(",")
            if len(valores) == 6:
                pot_x = int(valores[0])
                pot_y = int(valores[1])
                botao_2 = int(valores[2])
                botao_4 = int(valores[3])
                botao_7 = int(valores[4])
                botao_8 = int(valores[5])

                if abs(pot_x - 512) > 50:
                    comands["mover_x"] += round((pot_x - 512) / 300)
                if abs(pot_y - 512) > 50:
                    comands["mover_y"] += round((pot_y - 512) / 300)
                if botao_2 == 0:
                    comands["shot_button"] = True
                if botao_7 == 0:
                    comands["Next"] = True
                if botao_8 == 0:
                    comands["Before"] = True
                if botao_4 == 0:
                    comands["Enter"] = True
        except:
            pass

    # Aplicando cooldown
    tempo_atual = time.time()
    for tecla in ["Next", "Before", "Enter"]:
        if comands[tecla]:
            if tempo_atual - cooldowns[tecla] < cooldown_delay:
                comands[tecla] = False
            else:
                cooldowns[tecla] = tempo_atual

    # Normalizando direção para -1, 0 ou 1
    comands["mover_x"] = max(-1, min(1, comands["mover_x"]))
    comands["mover_y"] = max(-1, min(1, comands["mover_y"]))

    return comands
