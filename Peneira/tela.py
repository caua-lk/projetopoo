import pygame
from config import  reiniciar_jogo, criar_nave_escolhida
from const import Altura, Largura
import random

# --------------------------------------------------------------
# Otimização por meio de boas práticas ensinadas pela a IA

start_trial = pygame.image.load("sprites/FundoInicial.png").convert()
start_trial = pygame.transform.scale(start_trial,(Largura, Altura))

paused_trial = pygame.image.load("sprites/FundoPausado.png").convert()
paused_trial = pygame.transform.scale(paused_trial, (Largura,Altura))

playing_trial = pygame.image.load("sprites/FundoJogando01.png").convert()
playing_trial =  pygame.transform.scale(playing_trial, (Largura, Altura))
playing_life_trial = pygame.image.load("sprites/Life_icon.png").convert_alpha()
playing_life_trial = pygame.transform.scale(playing_life_trial, (32,32))

credits_trial = pygame.image.load("sprites/FundoCreditos.png").convert()
credits_trial = pygame.transform.scale(credits_trial, (Largura, Altura))
credits_text = [
                ["Desenvolvido por Cauã"],
                ["Arte e Design: Cauã"],
                ["Áudio: Cauã"],
                ["Por sua presença"],
                ["Muito Obrigado!"],
            ]

overgame_trial = [# Lista para sorteio de imagem para game over
                "sprites/gameoverV1.png",
                "sprites/gameoverV2.png",
                "sprites/gameoverV3.png",
            ]

select_trial = pygame.image.load("sprites/FundoJogando02.png")
select_trial = pygame.transform.scale(select_trial, (Largura, Altura))

Sprites = {
    "Penguim": pygame.image.load("sprites/NavePinguimDEF.png").convert_alpha(),
    "Ravage": pygame.image.load("sprites/NaveRavage.png").convert_alpha(),
    "Guns & Shot": pygame.image.load("sprites/NaveGunsShotDEF.png").convert_alpha(),
    "Warl": pygame.image.load("sprites/NaveWar.png").convert_alpha(),
    "Sniper": pygame.image.load("sprites/NaveSniper.png").convert_alpha()
}
# --------------------------------------------------------------
class Telas:

        def __init__(self, tela):

            self.tela = tela
            self.fonte = pygame.font.SysFont("Times New Roman", 50)

            # Tela inicial
            self.image_start = start_trial
            # Tela pausada
            self.image_paused = paused_trial
            # Tela jogando
            self.image_playing = playing_trial
            self.icon_life = playing_life_trial
            self.scroll_y = 0
            self.scroll_vel = 1
            # Tela de créditos
            self.image_credits = credits_trial
            # Texto dos créditos
            self.credito_texto = credits_text
            self.credito_texto_pos = Altura
            self.credito_texto_pos = -50  # Começa fora da tela, acima
            self.indice_atual = 0 
            # Tela de game over
            self.overgamer_images = overgame_trial
            imagem_escolhida = pygame.image.load(random.choice(overgame_trial)).convert()
            self.image_overgame = pygame.transform.scale(imagem_escolhida, (Largura, Altura))



            # Tela de seleção
            self.image_select = select_trial
            self.nave_selecionada = None
            self.naves_disponiveis = [
                {   # Seleção da Nave Pinguim
                    "Nome": "Penguim",
                    "sprites": Sprites["Penguim"],
                    "Descrição": "Nave equilibrada\ncriada pelo povo Pingu",
                    "stats": {"Velocidade": 5 , "Pontos de vida": 6 , "Dano": 2.5 , "Cadência":0.45}
                },
                {   # Seleção da Nave de Ataque
                    "Nome": "Ravage",
                    "sprites": Sprites["Ravage"],
                    "Descrição": "Nave veloz e agressiva\ncriada e desenvolvida\npelo povo Rusher",
                    "stats": {"Velocidade": 6 , "Pontos de vida": 5 , "Dano": 3.5 , "Cadência":0.4}
                },
                {   # Seleção da Nave Guns Shot
                    "Nome": "Guns & Shot",
                    "sprites": Sprites["Guns & Shot"],
                    "Descrição": "Nave com cadência rápida\ncom pouco dano\ne criada pelo povo Gunners",
                    "stats": {"Velocidade": 4 , "Pontos de vida": 5 , "Dano": 1.2 , "Cadência":0.25}
                },
                {   # Seleção da Nave de Guerra
                    "Nome": "Warl",
                    "sprites": Sprites["Warl"],
                    "Descrição": "Nave criada em prol da guerra\npelo povoado nobre de Crimson,\ncom suporte de grandes dores\ne constância no campo",
                    "stats": {"Velocidade": 3 , "Pontos de vida": 9 , "Dano": 2.2 , "Cadência":0.6}
                },
                {   # Seleção da Nave Espiã
                    "Nome": "Spectral Stealth",
                    "sprites": Sprites["Sniper"],
                    "Descrição": "Nave criada em prol da guerra\npelo povoado pobre de Crimson,\ncom dano letal e preciso",
                    "stats": {"Velocidade": 4 , "Pontos de vida": 5 , "Dano": 6 , "Cadência":1.2}
                },
                
            ]
            self.indice_nave_selecionada = 0
            self.nave_selecionada = self.naves_disponiveis[self.indice_nave_selecionada]
            # Dicionário com os botões que serão usados
            self.buttons = {
                "inicio": [
                    Button("Escolher", (Largura // 2, Altura // 2 + 200),
                        lambda estado: setattr(estado, "valor", "selecao"),
                        self.fonte, (255, 255, 0), (255, 0, 0)),

                    Button("Sair", (Largura // 2, Altura // 2 + 300),
                        lambda estado: pygame.quit(),
                        self.fonte, (255, 255, 0), (255, 0, 0)),

                    Button('.', (100,100),
                           lambda estado: setattr(estado, 'valor','credito'),
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

        # Carregamento do fundo do estado de jogo
        def Desenhar_Telas(self, estado_jogo, nave):
            if estado_jogo.valor == "inicio":

                self.tela.blit(self.image_start, (0, 0))

            elif estado_jogo.valor == "pausado":
                
                self.tela.blit(self.image_paused, (0, 0))

            elif estado_jogo.valor == "jogando":
                self.scroll_y += self.scroll_vel
                if self.scroll_y >= self.image_playing.get_height():
                    self.scroll_y = 0
                self.tela.blit(self.image_playing, (0, -self.scroll_y))
                self.tela.blit(self.image_playing, (0, self.image_playing.get_height()-self.scroll_y))
                # Mostrar quantas vidas a nave selecionada tem enquanto joga
                for life in range(nave.vida):
                        x = 20 + life * 36
                        self.tela.blit(self.icon_life, ( x, 20 ))

                font_HUD = pygame.font.SysFont("Arial", 34)
                texto_pontos = font_HUD.render(f"Pontos: {nave.points}", True, (255, 255, 0))
                self.tela.blit(texto_pontos, (20, 60))

            elif estado_jogo.valor == "credito":
                    self.tela.blit(self.image_credits, (0,0))

                    linhas_texto = self.credito_texto[self.indice_atual]
                    espaco = self.credito_texto_pos
                    for linha in linhas_texto:
                            escrito = self.fonte.render(linha, True, (255, 255, 255))
                            self.tela.blit(escrito, (self.tela.get_width() // 2 - escrito.get_width() // 2, espaco))
                            espaco += 55  # Espaço entre as linhas

                    # Quando o texto chega ao final, troca pelo próximo
                    if self.credito_texto_pos > Altura:
                        self.credito_texto_pos = -50  # Reinicia no topo
                        self.indice_atual += 1  # Passa para o próximo texto
                        
                        if self.indice_atual >= len(self.credito_texto): 
                            self.indice_atual = 0 

                    self.credito_texto_pos += 2
            elif estado_jogo.valor == "selecao":
                
                # Mostragem de status das naves disponivéis
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
                    sprite = nave["sprites"]
                    sprite = pygame.transform.scale(sprite, (128, 128))  # Garante tamanho padrão
                    self.tela.blit(sprite, (Largura // 2 + 100, y))
                    y += 140
                    descricao = nave["Descrição"]
                    lines = descricao.split("\n") # Quebra de linha para texto não ultrapassar a tela
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

            for botao in self.buttons.get(estado_jogo.valor, []):
                botao.draw(self.tela, pygame.mouse.get_pos())

        # Condicionamento da troca de telas
        def Alternar_telas(self, comands, estado_jogo, nave_jogada):
            estado_anterior = estado_jogo.valor
            new = None
            enemy = None
            # Apertar Enter para escolher nave
            if estado_jogo.valor == "inicio" and comands["Enter"]:

                estado_jogo.valor = "selecao"
            elif estado_jogo.valor == "selecao" and comands["Enter"] and self.nave_selecionada:
                estado_jogo.nave_escolhida = self.nave_selecionada
                estado_jogo.valor = "jogando"
                new, enemy = reiniciar_jogo()
            # Apertar ESC para pausar o jogo quando estiver jogando
            elif estado_jogo.valor == "jogando" and comands["Before"]:

                estado_jogo.valor =  "pausado"

            # Apertar ESC para voltar a jogar quando estiver pausado
            elif estado_jogo.valor == "pausado" and comands["Next"]:
                
                estado_jogo.valor = "jogando"

            elif estado_jogo.valor == "pausado" and comands["Enter"]:
                 estado_jogo.valor = "inicio"

            # Apertar ESC para sair dos créditos
            elif estado_jogo.valor == "credito" and comands["Before"]:
                
                estado_jogo.valor = "inicio"

            # Encerrar o jogo quando vida da nave escolhida estiver abaixo de zero
            elif estado_jogo.valor == "jogando" and nave_jogada.vida <= 0:
                self.randomize_gameover() # Sorteio da tela de fundo
                estado_jogo.valor = "Gameover"

            # Apertar Enter para retornar ao inicio do jogo
            elif estado_jogo.valor == "Gameover" and comands["Enter"]:

                estado_jogo.valor = "inicio"
            if estado_jogo.valor != estado_anterior:
                if estado_jogo.valor == "credito":
                    self.credito_texto_pos = Altura 
            return estado_jogo, new, enemy
        def selecionar_nave(self, index, estado_jogo):

            self.nave_selecionada = self.naves_disponiveis[index]

        def confirmar_nave(self, estado_jogo):
            if self.nave_selecionada:
                estado_jogo.nave_escolhida = self.nave_selecionada
                estado_jogo.valor = "jogando"  
                return reiniciar_jogo()  # Retorna nave e inimigos
        def randomize_gameover(self):
            # lógica de alternância entre fundos de game over
            value = random.choice(self.overgamer_images)

            self.image_overgame = pygame.image.load(value).convert()
            self.image_overgame = pygame.transform.scale(self.image_overgame, (Largura, Altura))
        def roll_nave(self, direcao,estado_jogo):
            total = len(self.naves_disponiveis)
            self.indice_nave_selecionada = (self.indice_nave_selecionada + direcao) % total
            self.nave_selecionada = self.naves_disponiveis[self.indice_nave_selecionada]
    # Estrutura base dos botões
    # TEXTO / CALLBACK / FONTE USADA / COR EM DESCANSO / COR QUANDO HOVER
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