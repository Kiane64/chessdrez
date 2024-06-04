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

        self.brancoMove = True
        self.movimentos = []

    def fazMove(self, move):
        self.tabuleiro[move.linInicial][move.colInicial] = "--"
        self.tabuleiro[move.linFinal][move.colFinal] = move.pecaMovida
        self.movimentos.append(move)
        self.brancoMove = not self.brancoMove


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

    def xadrezNotacao(self):
        return self.getRankFiles(self.linInicial, self.colInicial) + self.getRankFiles(
            self.linFinal, self.colFinal
        )

    def getRankFiles(self, l, c):
        return self.colstoFiles[c] + self.rowstoRank[l]
