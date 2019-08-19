import random

from board import Board, XO


class GameOrganizer:
    act_turn = 0
    winner = None

    def __init__(self, px, po, nplay=1, show_board=True, show_result=True, stat=100):
        self.px = px
        self.po = po
        self.players = {XO.PLAYER_X: px, XO.PLAYER_O: po}
        self.nwon = {XO.PLAYER_X: 0, XO.PLAYER_O: 0, XO.DRAW: 0}
        self.nplay = nplay
        self.board = None
        self.disp = show_board
        self.show_result = show_result
        self.turn = random.choice([XO.PLAYER_X, XO.PLAYER_O])
        self.nplayed = 0
        self.stat = stat

    @property
    def turn_player(self):
        return self.players[self.turn]

    def progress(self):
        while self.nplayed < self.nplay:
            self.board = Board()
            while self.board.winner is None:
                if self.disp: print("Turn is " + self.turn_player.name)
                act = self.turn_player.act(board=self.board, turn=self.turn)
                self.board.move(act, self.turn)
                if self.disp:
                    self.board.print_board()

                if self.board.winner is not None:
                    # notice every player that game ends
                    for player in self.players.values():
                        player.get_game_result(self.board, self.turn)
                    if self.board.winner == XO.DRAW:
                        if self.show_result:
                            print("Draw Game")
                    elif self.board.winner == self.turn:
                        out = "Winner : " + self.turn_player.name
                        if self.show_result:
                            print(out)
                    else:
                        print("Invalid Move!")

                    self.nwon[self.board.winner] += 1
                else:
                    self.switch_player()
                    # Notice other player that the game is going
                    self.turn_player.get_game_result(self.board, self.turn)

            self.nplayed += 1
            if self.nplayed % self.stat == 0 or self.nplayed == self.nplay:
                print(f"{self.px.name}: {self.nwon[XO.PLAYER_X]}, {self.po.name}: {self.nwon[XO.PLAYER_O]}, DRAW: {self.nwon[XO.DRAW]}")

    def switch_player(self):
        self.turn = self.turn.opponent
