"""
Aqui está nosso principal, será responsável por nos mostrar o jogo
"""

import pygame as p
import Engine
import colorama

colorama.init()

LARGURA = ALTURA = 712
DIMENSAO = 8
SQ_SIZE = ALTURA // DIMENSAO
FPS = 60
IMAGENS = {}
bl = 5

"""
Aqui estara nosso dicionario de imagens, carregadas apenas uma vez para não causar lag
"""


def carregarImagens():
    peças = ["Tp", "Cp", "Bp", "Qp", "Kp", "Pp", "Tb", "Cb", "Bb", "Qb", "Kb", "Pb"]
    for peça in peças:
        IMAGENS[peça] = p.transform.scale(p.image.load("chess/chessimages/" + peça + ".png"), (SQ_SIZE, SQ_SIZE))
        # podemos chamar qualquer peça usando IMAGENS["nome da peça"]


"""
Nosso PRINCIPAL, tera as informações que o jogador colocara e os graphics brrooo
"""


def main():
    p.init()
    tela = p.display.set_mode((LARGURA, ALTURA))
    clock = p.time.Clock()
    gs = Engine.GameState()
    movalido = gs.movimentoValido()
    moveFeito = False

    carregarImagens()  # antes do loop
    running = True
    quadradoSelec = ()  # seleção de quadrado no jogo, rastreia o ultimo click do mouse(tuple: (lin,col))
    cliqueJogador = []  # rastreia o click do jogador (dois tuple: [(6,4),(4,4)])

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # Mouse
            elif e.type == p.MOUSEBUTTONDOWN:  # hora de trabalhar com o mouse
                localizacao = p.mouse.get_pos()  # pega as coordenadas do mouse(x,y)
                col = localizacao[0] // SQ_SIZE
                lin = localizacao[1] // SQ_SIZE

                if quadradoSelec == (
                    lin,
                    col,
                ):  # clicando duas vezes no mesmo quadrado?
                    quadradoSelec = ()  # desseleciona
                    cliqueJogador = []  # reinicia o clique do jogador
                else:
                    quadradoSelec = (lin, col)
                    cliqueJogador.append(quadradoSelec)  # primeiro e segundo clique

                if len(cliqueJogador) == 2:  # movimento
                    move = Engine.Move(cliqueJogador[0], cliqueJogador[1], gs.tabuleiro)
                    print(move.xadrezNotacao())
                    for i in range(len(movalido)):
                        if move == movalido[i]:
                            gs.fazMove(movalido[i])
                            moveFeito = True
                            quadradoSelec = ()
                            cliqueJogador = []
                    if not moveFeito:
                        cliqueJogador = [quadradoSelec]

            # teclado
            if e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.desMove()
                    moveFeito = True
        if moveFeito:
            movalido = gs.movimentoValido()
            moveFeito = False

        drawGameState(tela, gs, movalido, quadradoSelec)
        clock.tick(FPS)
        p.display.flip()


"""
Responsável por toda visualização
"""


def Ilumination(tela, gs, movalido, quadradoSelec):
    if quadradoSelec != ():
        l, c = quadradoSelec
        if gs.tabuleiro[l][c][1] == ("b" if gs.brancoMove else "p"):  # peça quue pode ser movida
            # peça selecionado
            s = p.Surface((SQ_SIZE - (bl * 2), SQ_SIZE - (bl * 2)))
            s.fill(p.Color("red4"))
            tela.blit(s, (c * SQ_SIZE + bl, l * SQ_SIZE + bl))

            # movimento da peça
            s.fill(p.Color("gold2"))
            for move in movalido:
                if move.linInicial == l and move.colInicial == c:
                    tela.blit(
                        s,
                        (move.colFinal * SQ_SIZE + bl, move.linFinal * SQ_SIZE + bl),
                    )


def drawGameState(tela, gs, movalido, quadradoSelec):
    desenharTab(tela)  # desenha os quadrados do tabuleiro
    Ilumination(tela, gs, movalido, quadradoSelec)  # Desenha o highlight da peça e movimento dela
    desenharPeças(tela, gs.tabuleiro)  # advinha


def desenharTab(tela):
    cors = [p.Color("#eeddff"), p.Color("#4835f4")]
    for l in range(DIMENSAO):
        for c in range(DIMENSAO):
            cor = cors[(l + c) % 2]
            p.draw.rect(tela, cor, p.Rect(c * SQ_SIZE, l * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def desenharPeças(tela, tabuleiro):
    for l in range(DIMENSAO):
        for c in range(DIMENSAO):
            peça = tabuleiro[l][c]
            if peça != "--":
                tela.blit(IMAGENS[peça], p.Rect(c * SQ_SIZE, l * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
