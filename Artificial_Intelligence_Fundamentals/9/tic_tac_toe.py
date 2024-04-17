from easyAI import TwoPlayerGame, AI_Player, Negamax
from easyAI.Player import Human_Player


class GameController(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        self.nplayer = 1
        self.board = [0] * 9
        self.nopponent = 3 - self.nplayer
        self.play()

    def possible_moves(self):
        return [a + 1 for a, b in enumerate(self.board) if b == 0]

    def make_move(self, move):
        self.board[int(move) - 1] = self.nplayer

    def win_condition(self):
        possible_combinations = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
                                 [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]

        return any([all([(self.board[i - 1] == self.nplayer)
                         for i in combination]) for combination in possible_combinations])

    def is_over(self):
        return self.win_condition() or (self.possible_moves() == [])

    def show(self):
        print('\n' + '\n'.join([' '.join([['.', 'O', 'X'][self.board[3 * j + i]]
                                          for i in range(3)]) for j in range(3)]))

    def scoring(self):
        return 100 if self.win_condition() else 0

    def current_player(self):
        return self.nplayer

    def play(self):
        while not self.is_over():
            print("Possible moves: " + str(self.possible_moves()))
            self.show()
            move = self.players[self.nplayer - 1].ask_move(self)
            self.make_move(move)
            self.nplayer = 3 - self.nplayer

        self.show()
        print("Game over")
        if self.win_condition():
            print("Player", self.nplayer, "wins!")
        else:
            print("It's a tie!")



if __name__ == "__main__":
    algorithm = Negamax(9)

    while True:
        gc = GameController([Human_Player(), AI_Player(algorithm)])
        gc.play()
        play_again = input("Do you want to play again? (y/n): ")
        if play_again.lower() != 'y':
            break
