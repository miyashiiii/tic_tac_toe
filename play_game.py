from game_organizer import GameOrganizer
from player import PlayerHuman
from player_ql import PlayerQL


def play_game():
    p1 = PlayerHuman()
    p2 = PlayerQL()
    game = GameOrganizer(p1, p2)
    game.progress()


if __name__ == "__main__":
    play_game()
