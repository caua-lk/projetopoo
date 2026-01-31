import pygame
from config import reiniciar_jogo, criar_nave_escolhida
from const import Altura, Largura
import random
import time

# --------------------------------------------------------------
# Carregamento de imagens
start_trial = pygame.image.load("Jogo/sprites/FundoInicial.png").convert()
start_trial = pygame.transform.scale(start_trial,(Largura, Altura))

paused_trial = pygame.image.load("Jogo/sprites/FundoPausado.png").convert()
paused_trial = pygame.transform.scale(paused_trial, (Largura,Altura))

playing_trial = pygame.image.load("Jogo/sprites/FundoJogando01.png").convert()
playing_trial =  pygame.transform.scale(playing_trial, (Largura, Altura))
playing_life_trial = pygame.image.load("Jogo/sprites/Life_icon.png").convert_alpha()
playing_life_trial = pygame.transform.scale(playing_life_trial, (32,32))

credits_trial = pygame.image.load("Jogo/sprites/FundoCreditos.png").convert()
credits_trial = pygame.transform.scale(credits_trial, (Largura, Altura))
credits_text = [
    ["Desenvolvido por Cauã"],
    ["Arte e Design: Cauã"],
    ["Áudio: Cauã"],
    ["Por sua presença"],
    ["Muito Obrigado!"],
]

overgame_trial = [
    "Jogo/sprites/gameoverV1.png",
    "Jogo/sprites/gameoverV2.png",
    "Jogo/sprites/gameoverV3.png",
]

select_trial = pygame.image.load("Jogo/sprites/FundoJogando02.png")
select_trial = pygame.transform.scale(select_trial, (Largura, Altura))

Sprites = {
    "Penguim": pygame.image.load("Jogo/sprites/NavePinguimDEF.png").convert_alpha(),
    "Ravage": pygame.image.load("Jogo/sprites/NaveRavage.png").convert_alpha(),
    "Guns & Shot": pygame.image.load("Jogo/sprites/NaveGunsShotDEF.png").convert_alpha(),
    "Warl": pygame.image.load("Jogo/sprites/NaveWar.png").convert_alpha(),
    "Sniper": pygame.image.load("Jogo/sprites/NaveSniper.png").convert_alpha()
}

# --------------------------------------------------------------
class Telas:

    def __init__(self, tela):
        self.tela = tela
        self.fonte = pygame.font.SysFont("Times New Roman", 50)

        # Telas
        self.image_start = start_trial
        self.image_paused = paused_trial
        self.image_playing = playing_trial
        self.icon_life = playing_life_trial
        self.scroll_y = 0
        self.scroll_vel = 1
        self.image_credits = credits_trial
        self.credito_texto = credits_text
        self.credito_texto_pos = -50
        self.indice_atual = 0
        self.overgamer_images = overgame_trial
        imagem_escolhida = pygame.image.load(random.choice(overgame_trial)).convert()
        self.image_overgame = pygame.transform.scale(imagem_escolhida, (Largura, Altura))
        self.image_select = select_trial

        # Naves
        self.naves_disponiveis = [
            {"Nome": "Penguim", "Jogo/sprites": Sprites["Penguim"],
             "Descrição": "Nave equilibrada\ncriada pelo povo Pingu",
             "stats": {"Velocidade": 5 , "Pontos de vida": 6 , "Dano": 2.5 , "Cadência":0.45}},
            {"Nome": "Ravage", "Jogo/sprites": Sprites["Ravage"],
             "Descrição": "Nave veloz e agressiva\ncriada e desenvolvida\npelo povo Rusher",
             "stats": {"Velocidade": 6 , "Pontos de vida": 5 , "Dano": 3.5 , "Cadência":0.4}},
            {"Nome": "Guns & Shot", "Jogo/sprites": Sprites["Guns & Shot"],
             "Descrição": "Nave com cadência rápida\ncom pouco dano\ne criada pelo povo Gunners",
             "stats": {"Velocidade": 4 , "Pontos de vida": 5 , "Dano": 1.2 , "Cadência":0.25}},
            {"Nome": "Warl", "Jogo/sprites": Sprites["Warl"],
             "Descrição": "Nave criada em prol da guerra\npelo povoado nobre de Crimson",
             "stats": {"Velocidade": 3 , "Pontos de vida": 9 , "Dano": 2.2 , "Cadência":0.6}},
            {"Nome": "Spectral Stealth", "Jogo/sprites": Sprites["Sniper"],
             "Descrição": "Nave criada em prol da guerra\ncom dano letal e preciso",
             "stats": {"Velocidade": 4 , "Pontos de vida": 5 , "Dano": 6 , "Cadência":1.2}},
        ]
        self.indice_nave_selecionada = 0
        self.nave_selecionada = self.naves_disponiveis[self.indice_nave_selecionada]

        # Botões
        self.buttons = {
            "inicio": [
                Button("Escolher", (Largura // 2, Altura // 2 + 200),
                       lambda estado: setattr(estado, "valor", "selecao"),
                       self.fonte, (255, 255, 0), (255, 0, 0)),

                Button("Sair", (Largura // 2, Altura // 2 + 300),
                       lambda estado: pygame.quit(),
                       self.fonte, (255, 255, 0), (255, 0, 0)),

                Button('.', (100,100),
                       lambda estado: (
                           setattr(estado, 'valor','segredo'),
                           setattr(self,'easter_index',0),
                           setattr(self,'easter_timer',time.time())
                       ),
                       self.fonte, (0,0,0,255), (0,0,0,0), see=False)
            ],
            "Gameover": [
                Button("Tentar Novamente", (Largura // 2, 100),
                       lambda estado: setattr(estado, "valor", "inicio"),
                       self.fonte, (255, 255, 255), (255, 0, 0))
            ],
            "pausado": [
                Button("Continuar", (Largura // 2, Altura // 2 - 60),
                       lambda estado: setattr(estado, "valor", "jogando"),
                       self.fonte, (255, 255, 255), (0, 255, 0)),

                Button("Sair para Menu", (Largura // 2, Altura // 2 + 60),
                       lambda estado: setattr(estado, "valor", "inicio"),
                       self.fonte, (255, 255, 255), (255, 0, 0))
            ],
            "selecao": [
                Button("Confirmar Escolha", (Largura // 2, Altura - 100),
                       lambda estado: self.confirmar_nave(estado),
                       self.fonte, (255, 255, 255), (0, 255, 0))
            ]
        }
        for i, nave in enumerate(self.naves_disponiveis):
            botao = Button(
                nave["Nome"],
                (Largura // 4, 150 + i * 80),
                lambda estado, i=i: self.selecionar_nave(i, estado),
                self.fonte,
                (255, 255, 255),
                (0, 255, 0)
            )
            self.buttons["selecao"].append(botao)

        # Frames do segredo
        self.frames_easter_ovo = [
            pygame.image.load(f"Jogo/sprites/easter/frame{i}.png")
            for i in range(1, 38)
        ]
        self.easter_index = 0
        self.easter_timer = time.time()
        self.easter_intervalo = 0.15

    def Desenhar_Telas(self, estado_jogo, nave):
        if estado_jogo.valor == "inicio":
            self.tela.blit(self.image_start, (0, 0))

        elif estado_jogo.valor == "pausado":
            self.tela.blit(self.image_paused, (0, 0))

        elif estado_jogo.valor == "jogando" or estado_jogo.valor == 'Boss':
            self.scroll_y += self.scroll_vel
            if self.scroll_y >= self.image_playing.get_height():
                self.scroll_y = 0
            self.tela.blit(self.image_playing, (0, -self.scroll_y))
            self.tela.blit(self.image_playing, (0, self.image_playing.get_height()-self.scroll_y))
            for life in range(nave.vida):
                x = 20 + life * 36
                self.tela.blit(self.icon_life, (x, 20))
            font_HUD = pygame.font.SysFont("Arial", 34)
            texto_pontos = font_HUD
            texto_pontos = font_HUD.render(f"Pontos: {nave.points}", True, (255, 255, 0))
            self.tela.blit(texto_pontos, (20, 60))

        elif estado_jogo.valor == "credito":
            self.tela.blit(self.image_credits, (0,0))
            linhas_texto = self.credito_texto[self.indice_atual]
            espaco = self.credito_texto_pos
            for linha in linhas_texto:
                escrito = self.fonte.render(linha, True, (255, 255, 255))
                self.tela.blit(escrito, (self.tela.get_width() // 2 - escrito.get_width() // 2, espaco))
                espaco += 55

            if self.credito_texto_pos > Altura:
                self.credito_texto_pos = -50
                self.indice_atual += 1
                if self.indice_atual >= len(self.credito_texto):
                    self.indice_atual = 0
            self.credito_texto_pos += 2

        elif estado_jogo.valor == "segredo":
            if self.easter_index < len(self.frames_easter_ovo) - 1:   # só avança se não for o último
                if time.time() - self.easter_timer > self.easter_intervalo: 
                    self.easter_index += 1
                    self.easter_timer = time.time()

            # Desenha sempre o frame atual
            frame = self.frames_easter_ovo[self.easter_index]
            frame = pygame.transform.scale(frame, (Largura, Altura))
            self.tela.blit(frame, (0,0))

        elif estado_jogo.valor == "selecao":
            self.tela.blit(self.image_select, (0, 0))
            title = self.fonte.render("Escolha sua Nave", True, (255,255,255))
            self.tela.blit(title, (Largura // 2 - title.get_width() // 2 , 30))
            if self.nave_selecionada:
                nave = self.nave_selecionada
                y = 150
                fonte_info = pygame.font.SysFont("Times New Roman", 30)
                nome = fonte_info.render(nave["Nome"], True, (255, 255, 255))
                self.tela.blit(nome, (Largura // 2 + 100, y))
                y += 40
                sprite = nave["Jogo/sprites"]
                sprite = pygame.transform.scale(sprite, (128, 128))
                self.tela.blit(sprite, (Largura // 2 + 100, y))
                y += 140
                descricao = nave["Descrição"]
                lines = descricao.split("\n")
                for stat, valor in nave["stats"].items():
                    stat_texto = fonte_info.render(f"{stat}: {valor}", True, (255, 255, 255))
                    self.tela.blit(stat_texto, (Largura // 2, y))
                    y += 40
                for line in lines:
                    desc_render = fonte_info.render(line, True, (200,200,200))
                    self.tela.blit(desc_render,(Largura // 2 , y))
                    y += 40

        elif estado_jogo.valor == "Gameover":
            self.tela.blit(self.image_overgame, (0, 0))
            texto = self.fonte.render("Game Over", True, (200 , 200 , 200))
            text_rect = texto.get_rect(center=(self.tela.get_width() // 2, 50))
            self.tela.blit(texto, text_rect)

        # Desenha botões do estado atual
        for botao in self.buttons.get(estado_jogo.valor, []):
            botao.draw(self.tela, pygame.mouse.get_pos())

    # Alternar telas
    def Alternar_telas(self, comands, estado_jogo, nave_jogada):
        estado_anterior = estado_jogo.valor
        new = None
        enemy = None

        if estado_jogo.valor == "inicio" and comands["Enter"]:
            estado_jogo.valor = "selecao"

        elif estado_jogo.valor == "selecao" and comands["Enter"] and self.nave_selecionada:
            estado_jogo.nave_escolhida = self.nave_selecionada
            estado_jogo.valor = "jogando"
            new, enemy = reiniciar_jogo()

        elif comands['EasterEgg']:
            estado_jogo.valor = "credito"

        elif estado_jogo.valor == "credito" and comands['Before']:
            estado_jogo.valor = "inicio"
            comands['EasterEgg'] = False 

        elif (estado_jogo.valor == 'segredo' and comands['Before']):
            estado_jogo.valor = 'inicio'

        elif (estado_jogo.valor == "jogando" or estado_jogo.valor == 'Boss') and comands["Before"]:
            estado_jogo.valor = "pausado"

        elif estado_jogo.valor == "pausado" and comands["Next"]:
            estado_jogo.valor = "jogando"

        elif estado_jogo.valor == "pausado" and comands["Enter"]:
            estado_jogo.valor = "inicio"

        elif estado_jogo.valor == "credito" and comands["Before"]:
            estado_jogo.valor = "inicio"

        elif estado_jogo.valor == "jogando" and nave_jogada.vida <= 0:
            self.randomize_gameover()
            estado_jogo.valor = "Gameover"

        elif estado_jogo.valor == "Gameover" and comands["Enter"]:
            estado_jogo.valor = "inicio"

        # Reset ao entrar em segredo
        if estado_jogo.valor != estado_anterior:
            if estado_jogo.valor == "credito":
                self.credito_texto_pos = Altura 
            elif estado_jogo.valor == "segredo":
                self.easter_index = 0
                self.easter_timer = time.time()
    

        return estado_jogo, new, enemy

    def selecionar_nave(self, index, estado_jogo):
        self.nave_selecionada = self.naves_disponiveis[index]

    def confirmar_nave(self, estado_jogo):
        if self.nave_selecionada:
            estado_jogo.nave_escolhida = self.nave_selecionada
            estado_jogo.valor = "jogando"  
            return reiniciar_jogo()

    def randomize_gameover(self):
        value = random.choice(self.overgamer_images)
        self.image_overgame = pygame.image.load(value).convert()
        self.image_overgame = pygame.transform.scale(self.image_overgame, (Largura, Altura))

    def roll_nave(self, direcao,estado_jogo):
        total = len(self.naves_disponiveis)
        self.indice_nave_selecionada = (self.indice_nave_selecionada + direcao) % total
        self.nave_selecionada = self.naves_disponiveis[self.indice_nave_selecionada]

# --------------------------------------------------------------
# Estrutura base dos botões
class Button:
    def __init__(self, text, pos, callback, font, default_color, highlight_color, see = True):
        self.text = text
        self.callback = callback
        self.font = font
        self.default_color = default_color
        self.highlight_color = highlight_color
        self.label = self.font.render(self.text, True, self.default_color)
        self.rect = self.label.get_rect(center=pos)
        self.see = see

    def draw(self, surface, mouse_pos):
        if not self.see:
            return
        if self.rect.collidepoint(mouse_pos):
            label = self.font.render(self.text, True, self.highlight_color)
        else:
            label = self.label
        surface.blit(label, self.rect)
