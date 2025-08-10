import pygame 
from config import larguracreini,Alturacreini
pygame.init()
tela = pygame.display.set_mode((larguracreini , Alturacreini))
estado_jogo = "credito"
class Telas:
    def __init__(self, tela):
        self.tela = tela
        self.fonte = pygame.font.SysFont("Times New Roman", 50)
        self.credito_texto = [
            ["Desenvolvido por Cauã"],
            ["Arte e Design: Cauã"],
            ["Áudio: Cauã"],
            ["Ideia de Jogo: Giovanna Luz"],
             ["Muito Obrigado!"],
        ]
        self.credito_texto_pos = -50  # Começa fora da tela, acima
        self.indice_atual = 0  # Exibe apenas um texto por vez

    def Desenhar_Telas(self, estado_jogo):
        if estado_jogo == "credito":
            self.tela.fill((0, 0, 0))

            linhas_texto = self.credito_texto[self.indice_atual]
            espaco = self.credito_texto_pos
            for linha in linhas_texto:
                    escrito = self.fonte.render(linha, True, (255, 255, 255))
                    self.tela.blit(escrito, (self.tela.get_width() // 2 - escrito.get_width() // 2, espaco))
                    espaco += 55  # Espaço entre as linhas

            # Quando o texto chega ao final, troca pelo próximo
            if self.credito_texto_pos > Alturacreini:
                self.credito_texto_pos = -50  # Reinicia no topo
                self.indice_atual += 1  # Passa para o próximo texto
                
                if self.indice_atual >= len(self.credito_texto): 
                    self.indice_atual = 0 

            self.credito_texto_pos += 0.2
tela_fodona = Telas(tela)
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False  # Fecha o jogo ao clicar no "X"

    tela_fodona.Desenhar_Telas(estado_jogo)  
    pygame.display.update()

pygame.quit()