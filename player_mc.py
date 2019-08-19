import random

from player import Player


class PlayerMC(Player):
    def __init__(self):
        name = "MC"
        super().__init__(name)

    def win_or_rand(self, board, turn):
        acts = board.get_possible_pos()
        # see only next winnable act
        for act in acts:
            tempboard = board.clone()
            tempboard.move(act, turn)
            # check if win
            if tempboard.winner == turn:
                return act
        i = random.randrange(len(acts))
        return acts[i]

    def get_act_score(self, board, act, turn):
        tempboard = board.clone()
        tempboard.move(act, turn)
        tempturn = turn
        while tempboard.winner is None:
            tempturn = tempturn * -1
            tempboard.move(self.win_or_rand(tempboard, tempturn), tempturn)

        if tempboard.winner == turn:
            return 1
        else:
            return -1

    def act(self, board, turn):
        acts = board.get_possible_pos()
        scores = {}
        n = 50
        for act in acts:
            act_score = 0
            for i in range(n):
                # print("Try"+str(i))
                act_score += self.get_act_score(board, act, turn)

                # print(scores)
            act_score /= n
            scores.append(act_score)

        max_score = max(scores.values())
        for act, v in scores.items():
            if v == max_score:
                # print(str(act)+"="+str(v))
                return act
