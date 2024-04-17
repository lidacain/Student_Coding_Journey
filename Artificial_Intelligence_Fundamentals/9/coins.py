from easyAI import TwoPlayerGame, Human_Player, AI_Player, TranspositionTable
from easyAI.AI import solve_with_iterative_deepening


class LastCoinStanding(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        self.nplayer = 1
        self.num_coins = 25
        self.max_coins = 4

    def possible_moves(self):
        return [str(x) for x in range(1, self.max_coins + 1)]

    def make_move(self, move):
        self.num_coins -= int(move)

    def win(self):
        return self.num_coins <= 0

    def is_over(self):
        return self.win()

    def scoring(self):
        return 100 if self.win() else 0

    def show(self):
        print(self.num_coins, 'coins left in the pile')

    def current_player(self):
        return self.nplayer



if __name__ == "__main__":
    tt = TranspositionTable()

    LastCoinStanding.ttentry = lambda self: self.num_coins

    result, depth, move = solve_with_iterative_deepening(
        LastCoinStanding([AI_Player(tt), Human_Player()]),
        range(2, 20),
        win_score=100,
        tt=tt
    )
    print(result, depth, move)

    game = LastCoinStanding([AI_Player(tt), Human_Player()])
    game.play()
