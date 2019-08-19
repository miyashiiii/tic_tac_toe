from enum import Enum


#
# EMPTY = 0
# PLAYER_X = 1
# PLAYER_O = -1
# MARKS = {PLAYER_X: "X", PLAYER_O: "O", EMPTY: " "}
# DRAW = 2


class XO(Enum):
    EMPTY = 0
    PLAYER_X = 1
    PLAYER_O = -1
    DRAW = 2

    def __str__(self):
        if self is self.PLAYER_X:
            return "X"
        if self is self.PLAYER_O:
            return "O"
        if self is self.EMPTY:
            return " "
        raise

    @property
    def opponent(self):
        if self is self.PLAYER_X:
            return self.PLAYER_O
        if self is self.PLAYER_O:
            return self.PLAYER_X
        raise


class Board:

    def __init__(self, board=None):
        if board is None:
            self.board = []
            for i in range(9):
                self.board.append(XO.EMPTY)
        else:
            self.board = board
        self.winner = None

    def get_possible_pos(self):
        pos = []
        for i in range(9):
            if self.board[i] == XO.EMPTY:
                pos.append(i)
        return pos

    def print_board(self):
        tempboard = []
        for xo in self.board:
            tempboard.append(xo)
        row = ' {} | {} | {} '
        hr = '\n-----------\n'
        print((row + hr + row + hr + row).format(*tempboard))

    def check_winner(self):
        win_cond = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7))
        for each in win_cond:
            if self.board[each[0] - 1] == self.board[each[1] - 1] == self.board[each[2] - 1]:
                if self.board[each[0] - 1] != XO.EMPTY:
                    self.winner = self.board[each[0] - 1]
                    return self.winner
        return None

    def check_draw(self):
        if len(self.get_possible_pos()) == 0 and self.winner is None:
            self.winner = XO.DRAW
            return XO.DRAW
        return None

    def move(self, pos, player):
        if self.board[pos] == XO.EMPTY:
            self.board[pos] = player
        else:
            self.winner = player.opponent
        self.check_winner()
        self.check_draw()

    def clone(self):
        return Board(self.board.copy())
