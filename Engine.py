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
        pass

    def cavaloMoves(self, l, c, moves):
        pass

    def bispoMoves(self, l, c, moves):
        pass

    def rainhaMoves(self, l, c, moves):
        pass

    def reiMoves(self, l, c, moves):
        pass


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
        return self.getRankFiles(self.linInicial, self.colInicial) + self.getRankFiles(
            self.linFinal, self.colFinal
        )

    def getRankFiles(self, l, c):
        return self.colstoFiles[c] + self.rowstoRank[l]
