"""
Carrega toda a informação atual do xadrez, também determina os lances válidos do jogo
"""

import chess


class GameState:
    def __init__(self):
        # o tabuleiro é 8x8 sendo cada peça dois caracteres, os espaços vazios são dito com dois --
        # o primeiro caractere diz o nome da peça: "T" "C" "B" "Q" "K"
        # o segundo caractere diz a cor da peça: "P" "B"
        self.tabuleiro = [
            ["Tp", "Cp", "Bp", "Qp", "Kp", "Bp", "Cp", "Tp"],
            ["Pp", "Pp", "Pp", "Pp", "Pp", "Pp", "Pp", "Pp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb"],
            ["Tb", "Cb", "Bb", "Qb", "Kb", "Bb", "Cb", "Tb"],
        ]
        self.funcaoMovim = {
            "P": self.peaoMoves,
            "T": self.torreMoves,
            "C": self.cavaloMoves,
            "B": self.bispoMoves,
            "Q": self.rainhaMoves,
            "K": self.reiMoves,
        }

        self.brancoMove = True
        self.movimentos = []

    def fazMove(self, move):
        self.tabuleiro[move.linInicial][move.colInicial] = "--"
        self.tabuleiro[move.linFinal][move.colFinal] = move.pecaMovida
        self.movimentos.append(move)
        self.brancoMove = not self.brancoMove

    def desMove(self):
        if len(self.movimentos) != 0:  # verifica se tem movimento para desfazer
            move = self.movimentos.pop()
            self.tabuleiro[move.linInicial][move.colInicial] = move.pecaMovida
            self.tabuleiro[move.linFinal][move.colFinal] = move.pecaCapturada
            self.brancoMove = not self.brancoMove

    def movimentoValido(self):
        return self.movimentoPossivel()

    def movimentoPossivel(self):
        moves = []
        for l in range(len(self.tabuleiro)):
            for c in range(len(self.tabuleiro[l])):
                turno = self.tabuleiro[l][c][1]
                if (turno == "b" and self.brancoMove) or (
                    turno == "p" and not self.brancoMove
                ):
                    peca = self.tabuleiro[l][c][0]
                    self.funcaoMovim[peca](l, c, moves)
        return moves

    def peaoMoves(self, l, c, moves):
        if self.brancoMove:  # movimento das peças brancas
            if self.tabuleiro[l - 1][c] == "--":  # avanço de uma casa do peão
                moves.append(Move((l, c), (l - 1, c), self.tabuleiro))
                if (
                    l == 6 and self.tabuleiro[l - 2][c] == "--"
                ):  # avanço de duas casas do peão
                    moves.append(Move((l, c), (l - 2, c), self.tabuleiro))

            if c - 1 >= 0:  # captura no lado esquerdo
                if self.tabuleiro[l - 1][c - 1][1] == "p":
                    moves.append(Move((l, c), (l - 1, c - 1), self.tabuleiro))
            if c + 1 <= 7:  # captura no lado direito
                if self.tabuleiro[l - 1][c + 1][1] == "p":
                    moves.append(Move((l, c), (l - 1, c + 1), self.tabuleiro))

        if not self.brancoMove:  # movimento das peças pretas
            if self.tabuleiro[l + 1][c] == "--":  # avanço de uma casa do peão
                moves.append(Move((l, c), (l + 1, c), self.tabuleiro))
                if (
                    l == 1 and self.tabuleiro[l + 2][c] == "--"
                ):  # avanço de duas casas do peão
                    moves.append(Move((l, c), (l + 2, c), self.tabuleiro))

            if c - 1 >= 0:  # captura no lado esquerdo
                if self.tabuleiro[l + 1][c - 1][1] == "b":
                    moves.append(Move((l, c), (l + 1, c - 1), self.tabuleiro))
            if c + 1 <= 7:  # captura no lado direito
                if self.tabuleiro[l + 1][c + 1][1] == "b":
                    moves.append(Move((l, c), (l + 1, c + 1), self.tabuleiro))

    def torreMoves(self, l, c, moves):
        direcoes = (
            (-1, 0),
            (0, -1),
            (1, 0),
            (0, 1),
        )  # Verifica cima, esquerda, baixo e direita
        corInimiga = "p" if self.brancoMove else "b"  # Ou peça preta ou peça branca
        for d in direcoes:
            for i in range(1, 8):
                linhaFim = l + d[0] * i
                colunaFim = c + d[1] * i
                if 0 <= linhaFim < 8 and 0 <= colunaFim < 8:  # Vê se esta no tabuleiro
                    pecaFim = self.tabuleiro[linhaFim][colunaFim]
                    if pecaFim == "--":  # Se vazio pode mover
                        moves.append(
                            Move((l, c), (linhaFim, colunaFim), (self.tabuleiro))
                        )
                    elif (
                        pecaFim[1] == corInimiga
                    ):  # Jeito mais rapido de verificar se a peça é do oponente ou não
                        moves.append(
                            Move((l, c), (linhaFim, colunaFim), (self.tabuleiro))
                        )
                        break  # Depois de verificar ele para de dar movimento válido
                    else:
                        break  # Verifica peça aliada e para
                else:  # Fora do tabuleiro
                    break

    def cavaloMoves(self, l, c, moves):
        cavaloMovimentos = (
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        )
        corAliada = "b" if self.brancoMove else "p"
        for m in cavaloMovimentos:
            linhaFim = l + m[0]
            colFim = c + m[1]
            if 0 <= linhaFim < 8 and 0 <= colFim < 8:
                pecaFim = self.tabuleiro[linhaFim][colFim]
                if pecaFim[1] != corAliada:
                    moves.append(Move((l, c), (linhaFim, colFim), (self.tabuleiro)))

    def bispoMoves(self, l, c, moves):
        diagonal = (
            (1, 1),
            (-1, 1),
            (1, -1),
            (-1, -1),
        )  # Verifica diagonais, o restante é igual a torre
        corInimiga = "p" if self.brancoMove else "b"
        for d in diagonal:
            for i in range(1, 8):
                linhaFim = l + d[0] * i
                colunaFim = c + d[1] * i
                if 0 <= linhaFim < 8 and 0 <= colunaFim < 8:
                    pecaFim = self.tabuleiro[linhaFim][colunaFim]
                    if pecaFim == "--":
                        moves.append(
                            Move((l, c), (linhaFim, colunaFim), (self.tabuleiro))
                        )
                    elif pecaFim[1] == corInimiga:
                        moves.append(
                            Move((l, c), (linhaFim, colunaFim), (self.tabuleiro))
                        )
                        break
                    else:
                        break
                else:
                    break

    def rainhaMoves(self, l, c, moves):
        self.torreMoves(l, c, moves)
        self.bispoMoves(l, c, moves)

    def reiMoves(self, l, c, moves):
        reiMovimentos = (
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        )
        corAliada = "b" if self.brancoMove else "p"
        for r in range(8):
            linhaFim = l + reiMovimentos[r][0]
            colFim = c + reiMovimentos[r][1]
            if 0 <= linhaFim < 8 and 0 <= colFim < 8:
                pecaFim = self.tabuleiro[linhaFim][colFim]
                if pecaFim[1] != corAliada:
                    moves.append(Move((l, c), (linhaFim, colFim), (self.tabuleiro)))


class Move:

    rankstoRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowstoRank = {v: k for k, v in rankstoRows.items()}
    filestoCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colstoFiles = {v: k for k, v in filestoCols.items()}

    def __init__(self, qdinicial, qdfinal, tabuleiro):
        self.linInicial = qdinicial[0]
        self.colInicial = qdinicial[1]
        self.linFinal = qdfinal[0]
        self.colFinal = qdfinal[1]
        self.pecaMovida = tabuleiro[self.linInicial][self.colInicial]
        self.pecaCapturada = tabuleiro[self.linFinal][self.colFinal]
        self.moveID = (
            self.linInicial * 1000
            + self.colInicial * 100
            + self.linFinal * 10
            + self.colFinal
        )

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def xadrezNotacao(self):
        return (
            self.getRankFiles(self.linInicial, self.colInicial).upper()
            + "-"
            + self.getRankFiles(self.linFinal, self.colFinal).upper()
        )

    def getRankFiles(self, l, c):
        return self.colstoFiles[c] + self.rowstoRank[l]
