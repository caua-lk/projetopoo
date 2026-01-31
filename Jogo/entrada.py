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
# Dicionário com mapeamentos por tipo de controle
controller_map = {
    "Xbox": {

        "axis_x": 0,   # analógico esquerdo X
        "axis_y": 1,   # analógico esquerdo Y
        "shot_button": 0,   # Botão A
        "Next": 1,          # Botão B
        "Before": 2,        # Botão X
        "Enter": 3          # Botão Y

    },
    "PS": {

        "axis_x": 0,   # analógico esquerdo X
        "axis_y": 1,   # analógico esquerdo Y
        "shot_button": 14,  # Botão X
        "Next": 15,         # Botão O
        "Before": 13,       # Botão Quadrado
        "Enter": 12         # Botão Triângulo

    },
    "Generic": {

        "axis_x": 0,
        "axis_y": 1,
        "shot_button": 0,
        "Next": 1,
        "Before": 2,
        "Enter": 3

    }
}

cooldown_delay = 0.3  # segundos

button_history = []
max_history = 10

easter_egg_command = ["shot_button", "Next", "Before", "Enter", "Before", "Next", "shot_button", "Next"]

def Check_history(): 
    if len(button_history) >= len(easter_egg_command): 
        return button_history[-len(easter_egg_command):] == easter_egg_command 
    return False
def detect(joystick):
    name = joystick.get_name().lower()
    if 'xbox' in name:
        return 'Xbox'
    elif 'playstation' in name or 'wireless' in name:
        return 'PS'
    else:
        return 'Generic'
def view_commands(joystick=None, arduino=None, map=None):
    if map is None:
        map = controller_map["Generic"]
    comands = {
        "mover_x": 0,
        "mover_y": 0,
        "shot_button": False,
        "Next": False,
        "Before": False,
        "Enter": False,
        "EasterEgg": False,
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
        if pressionada[pygame.K_SPACE]:
            comands["shot_button"] = True
        if pressionada[pygame.K_ESCAPE] or pressionada[pygame.K_b]:
            comands["Before"] = True
        if pressionada[pygame.K_CLEAR] or pressionada[pygame.K_n]:
            comands["Next"] = True
        if pressionada[pygame.K_RETURN]:
            comands["Enter"] = True

    # Controle USB
    if joystick:
        eixo_x = joystick.get_axis(map['axis_x'])
        eixo_y = joystick.get_axis(map['axis_y'])
        if abs(eixo_x) > 0.2:
            comands["mover_x"] += round(eixo_x)
        if abs(eixo_y) > 0.2:
            comands["mover_y"] += round(eixo_y)

        for button in ["shot_button", "Next", "Before", "Enter"]:
            if joystick.get_button(map[button]):
                comands[button] = True
                button_history.append(button)
                if len(button_history) > max_history:
                    button_history.pop(0)

        if Check_history():
            comands["EasterEgg"] = True

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
