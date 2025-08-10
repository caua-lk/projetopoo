import pygame
from config import Altura, Largura, larguracreini, Alturacreini

class Telas:
    def __init__(self, tela):
        self.tela = tela
        self.fonte = pygame.font.SysFont("Times New Roman", 50)

        # Tela inicial
        # self.imagem_fundo_inicio = pygame.image.load("caminho/para/inicio.png")
        # self.imagem_fundo_inicio = pygame.transform.scale(self.imagem_fundo_inicio, (larguracreini, Alturacreini))
        self.imagem_fundo_inicio = pygame.Surface((larguracreini, Alturacreini))
        self.imagem_fundo_inicio.fill((30, 30, 80))  # azul escuro

        # Tela pausada
        # self.imagem_fundo_pausado = pygame.image.load("caminho/para/pausado.png")
        # self.imagem_fundo_pausado = pygame.transform.scale(self.imagem_fundo_pausado, (Largura, Altura))
        self.imagem_fundo_pausado = pygame.Surface((Largura, Altura))
        self.imagem_fundo_pausado.fill((50, 50, 50))  # cinza escuro

        # Tela jogando
        # self.imagem_fundo_jogando = pygame.image.load("caminho/para/jogando.png")
        # self.imagem_fundo_jogando = pygame.transform.scale(self.imagem_fundo_jogando, (Largura, Altura))
        self.imagem_fundo_jogando = pygame.Surface((Largura, Altura))
        self.imagem_fundo_jogando.fill((0, 0, 0))  # preto

        # Tela de créditos
        # self.imagem_fundo_credito = pygame.image.load("caminho/para/credito.png")
        # self.imagem_fundo_credito = pygame.transform.scale(self.imagem_fundo_credito, (larguracreini, Alturacreini))
        self.imagem_fundo_credito = pygame.Surface((larguracreini, Alturacreini))
        self.imagem_fundo_credito.fill((20, 20, 100))  # azul mais claro

        self.credito_texto = [
            ["Desenvolvido por Cauã"],
            ["Arte e Design: Cauã"],
            ["Áudio: Cauã"],
            ["Ideia de Jogo: Giovanna Luz"],
             ["Muito Obrigado!"],
        ]
        self.credito_texto_pos = Alturacreini

    def Desenhar_Telas(self, estado_jogo):
        if estado_jogo == "inicio":
            self.tela.blit(self.imagem_fundo_inicio, (0, 0))
            textin = self.fonte.render("Pressione ENTER para iniciar", True, (255, 255, 0))
            self.tela.blit(textin, (self.tela.get_width() // 2 - 200, self.tela.get_height() // 2 - 25))

        elif estado_jogo == "pausado":
            self.tela.blit(self.imagem_fundo_pausado, (0, 0))
            textin = self.fonte.render("Pressione ESC para voltar ao jogo", True, (255, 255, 0))
            self.tela.blit(textin, (self.tela.get_width() // 2 - 200, self.tela.get_height() // 2 - 25))

        elif estado_jogo == "jogando":
            self.tela.blit(self.imagem_fundo_jogando, (0, 0))

        elif estado_jogo == "credito":
            self.tela.blit(self.imagem_fundo_credito, (0, 0))
            y = self.credito_texto_pos
            for linha in self.credito_texto:
                texto = self.fonte.render(linha, True, (255, 255, 255))
                self.tela.blit(texto, (self.tela.get_width() // 2 - 200, y))
                y += 60

    def Alternar_telas(self, tecla_pressionada, estado_jogo):
        if estado_jogo == "inicio" and tecla_pressionada == pygame.K_RETURN:
            return "jogando"
        elif estado_jogo == "jogando" and tecla_pressionada == pygame.K_ESCAPE:
            return "pausado"
        elif estado_jogo == "pausado" and tecla_pressionada == pygame.K_ESCAPE:
            return "jogando"
        elif estado_jogo == "credito" and tecla_pressionada == pygame.K_ESCAPE:
            return "inicio"
        return estado_jogo