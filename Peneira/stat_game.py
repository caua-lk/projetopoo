import pygame
pygame.init()
pygame.mixer.init()
class EstadoJogo:
    def __init__(self):
        self._valor = "inicio"
        self.nave_escolhida = None
        self.musica_atual = None

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, novo_valor):
        if self._valor != novo_valor:
            self._valor = novo_valor
            self.Tocar_musica()

    def Tocar_musica(self):
        musics = {
            "inicio": "Sounds/Inicio-Song.mp3",
            "credito": "Sounds/Creditos-Song.mp3",
            "Gameover": "Sounds/Gamover-Song.mp3"
        }

        Default = "Sounds/Default-Song.mp3"
        view = musics.get(self._valor, Default)

        if view != self.musica_atual:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(view)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
                self.musica_atual = view

estado_jogo = EstadoJogo()