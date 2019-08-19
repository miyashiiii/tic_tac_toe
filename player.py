import random

from board import XO


class Player:

    def __init__(self, name):
        self.name = name

    def act(self, board, turn):
        raise NotImplementedError

    def get_game_result(self, board, turn):
        pass


class PlayerRandom(Player):
    def __init__(self):
        name = "Random"
        super().__init__(name)

    def act(self, board, turn):
        acts = board.get_possible_pos()
        i = random.randrange(len(acts))
        return acts[i]


class PlayerHuman(Player):
    def __init__(self):
        name = "Human"
        super().__init__(name)

    def act(self, board, turn):
        valid = False
        while not valid:
            try:
                act = input(f"Where would you like to place {turn} (1-9)? ")
                act = int(act)
                # if act >= 1 and act <= 9 and board.board[act-1]==EMPTY:
                if 1 <= act <= 9:
                    valid = True
                    return act - 1
                else:
                    print("That is not a valid move! Please try again.")
            except Exception as e:
                print(act + "is not a valid move! Please try again.")
        return act

    def get_game_result(self, board, turn):
        if board.winner is not None and board.winner != turn and board.winner != XO.DRAW:
            print("I lost...")


class PlayerAlphaRandom(Player):
    def __init__(self):
        name = "AlphaRandom"
        super().__init__(name)

    def act(self, board, turn):
        acts = board.get_possible_pos()
        # see only next winnable act
        for act in acts:
            tempboard = board.clone()
            tempboard.move(act, turn)
            # check if win
            if tempboard.winner == turn:
                # print ("Check mate")
                return act
        i = random.randrange(len(acts))
        return acts[i]
