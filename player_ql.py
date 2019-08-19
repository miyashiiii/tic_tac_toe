import random

from board import XO
from player import Player


class PlayerQL(Player):
    def __init__(self, e=0.2, alpha=0.3):
        self.q = {}  # set of s,a
        self.e = e
        self.alpha = alpha
        self.gamma = 0.9
        self.last_move = None
        self.last_board = None
        self.total_game_count = 0
        name = "QL"
        super().__init__(name)

    def policy(self, board):
        self.last_board = board.clone()
        acts = board.get_possible_pos()
        # Explore sometimes
        if random.random() < (self.e / (self.total_game_count // 10000 + 1)):
            i = random.randrange(len(acts))
            return acts[i]
        qs = [self.get_q(tuple(self.last_board.board), act) for act in acts]
        max_q = max(qs)

        if qs.count(max_q) > 1:
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(acts)) if qs[i] == max_q]
            i = random.choice(best_options)
        else:
            i = qs.index(max_q)

        self.last_move = acts[i]
        return acts[i]

    def get_q(self, state, act):
        # encourage exploration; "optimistic" 1.0 initial values
        if self.q.get((state, act)) is None:
            self.q[(state, act)] = 1
        return self.q.get((state, act))

    def get_game_result(self, board, turn):
        if self.last_move is not None:
            if board.winner is None:
                self.learn(self.last_board, self.last_move, 0, board)
                pass
            else:
                if board.winner == turn:
                    self.learn(self.last_board, self.last_move, 1, board)
                elif board.winner != XO.DRAW:
                    self.learn(self.last_board, self.last_move, -1, board)
                else:
                    self.learn(self.last_board, self.last_move, 0, board)
                self.total_game_count += 1
                self.last_move = None
                self.last_board = None

    def learn(self, s, a, r, fs):
        pQ = self.get_q(tuple(s.board), a)
        if fs.winner is not None:
            max_q_new = 0
        else:
            max_q_new = max([self.get_q(tuple(fs.board), act) for act in fs.get_possible_pos()])
        self.q[(tuple(s.board), a)] = pQ + self.alpha * ((r + self.gamma * max_q_new) - pQ)
        # print (str(s.board)+"with "+str(a)+" is updated from "+str(pQ)+" refs MAXQ="+str(maxQnew)+":"+str(r))
        # print(self.q)

    def act(self, board, turn):
        return self.policy(board)
