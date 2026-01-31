from nave import Nave_Guns_Shot,Nave_sniper,Nave_tank,NaveAtaque,NavePenguim
from Inimigos import Maus
from stat_game import estado_jogo
def criar_nave_escolhida():
    if not estado_jogo.nave_escolhida or "Nome" not in estado_jogo.nave_escolhida:
        return NavePenguim()  # Fallback seguro
    nome = estado_jogo.nave_escolhida["Nome"]
    if nome == "Penguim":
        return NavePenguim()
    elif nome == "Ravage":
        return NaveAtaque()
    elif nome == "Guns & Shot":
        return Nave_Guns_Shot()
    elif nome == "Warl":
        return Nave_tank()
    elif nome == "Spectral Stealth":
        return Nave_sniper()
    else:
        return NavePenguim()  # Fallback
def reiniciar_jogo():
    nave = criar_nave_escolhida()
    inimigos = Maus()
    return nave, inimigos