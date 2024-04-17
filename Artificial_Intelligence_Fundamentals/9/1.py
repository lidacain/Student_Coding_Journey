# This is a variant of the Tic Tac Toe recipe given in the easyAI library

from easyAI import TwoPlayerGame, AI_Player, Negamax
from easyAI.Player import Human_Player


class GameController(TwoPlayerGame):
    def __init__(self, players):
        # Define the players
        self.players = players

        # Define who starts the game
        self.nplayer = 1

        # Define the board
        self.board = [0] * 9

        # Define the opponent
        self.nopponent = 3 - self.nplayer

        # Play the game
        self.play()

    def play(self):
        while not self.is_over():
            print("Possible moves: " + str(self.possible_moves()))
            self.show()
            move = self.players[self.nplayer - 1].ask_move(self)
            self.make_move(move)
            self.nplayer = 3 - self.nplayer


    # Define possible moves
    def possible_moves(self):
        return [a + 1 for a, b in enumerate(self.board) if b == 0]

    # Make a move
    def make_move(self, move):
        self.board[int(move) - 1] = self.nplayer

    # Does the opponent have three in a line?
    def loss_condition(self):
        possible_combinations = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
                                 [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]

        return any([all([(self.board[i - 1] == self.nopponent)
                         for i in combination]) for combination in possible_combinations])
        # Check if the game is over

    def is_over(self):
        return self.loss_condition() or self.possible_moves() == []

    def scoring(self):
        if self.loss_condition():
            return -100
        elif self.possible_moves() == []:
            return 0
        else:
            return -0.1

    # Show current position
    def show(self):
        print('\n' + '\n'.join([' '.join([['.', 'O', 'X'][self.board[3 * j + i]]
                                          for i in range(3)]) for j in range(3)]))

    def get_move(self, game):
        move = input("Enter your move: ")
        return move

    def current_player(self):
        return self.nplayer




if __name__ == "__main__":
    # Define the algorithm
    algorithm = Negamax(7)

    # Start the game
    gc = GameController([Human_Player(), AI_Player(algorithm)])
    gc.play()
