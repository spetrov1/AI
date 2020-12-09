
class TicTacToe:

    def __init__(self, chosenPlayer):
        if chosenPlayer not in ['X', 'O']:
            print('Invalid chosen player ... Could not start the tic tac toe')
            return
        self.human = chosenPlayer
        if (self.human == 'X'):
            self.computer = 'O'
        else:
            self.computer = 'X'

        self.initialize_game()

    def initialize_game(self):
        self.board = [['_','_','_'],
                      ['_','_','_'],
                      ['_','_','_']]

        # Player X always plays first
        self.player_turn = 'X'

    def display_board(self):
        for i in range(0, 3):
            for j in range(0, 3):
                print('{}|'.format(self.board[i][j]), end=" ")
            print()
        print()

    # Determines if the made move is a legal move
    def is_valid(self, x, y):
        if x < 0 or x > 2 or y < 0 or y > 2:
            return False
        elif self.board[x][y] != '_':
            return False
        else:
            return True

    # return X if min wins
    # return O if max wins
    # return None if not finished
    def get_eventual_winner(self):
        # check for vertical win
        for i in range(0, 3):
            if (self.board[0][i] != '_' and
                self.board[0][i] == self.board[1][i] and
                self.board[1][i] == self.board[2][i]):
                return self.board[0][i]

        # check for horizontal win
        for i in range(0, 3):
            if (self.board[i] == ['X', 'X', 'X']):
                return 'X'
            elif (self.board[i] == ['O', 'O', 'O']):
                return 'O'

        # check for main diagonal win
        if (self.board[0][0] != '_' and
            self.board[0][0] == self.board[1][1] and
            self.board[1][1] == self.board[2][2]):
            return self.board[0][0]

        # check for second diagonal win
        if (self.board[0][2] != '_' and
            self.board[0][2] == self.board[1][1] and
            self.board[1][1] == self.board[2][0]):
            return self.board[0][2]

        # if board not full then return None
        for i in range(0, 3):
            for j in range(0, 3):
                # There's an empty field, we continue the game
                if (self.board[i][j] == '_'):
                    return None

        # Game is equal!
        return '_'

    def max(self, alpha, beta):

        # maxv values:
        # -1 - loss
        # 0  - a tie
        # 1  - win

        # -2 is less than worst case (-1):
        maxv = -2

        x = None
        y = None

        result = self.get_eventual_winner()


        # check for terminated states
        fictiveCoordinate = -1
        if result == 'X':
            return (-1, fictiveCoordinate, fictiveCoordinate)
        elif result == 'O':
            return (1, fictiveCoordinate, fictiveCoordinate)
        elif result == '_':
            return (0, fictiveCoordinate, fictiveCoordinate)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[i][j] == '_':
                    self.board[i][j] = 'O'
                    (v, _, _) = self.min(alpha, beta)
                    # Fixing the maxv value if needed
                    if v > maxv:
                        maxv = v
                        x = i
                        y = j

                    if v >= beta:
                        self.board[i][j] = '_'
                        return (v, x, y)
                    
                    alpha = max(alpha, v)

                    # Setting back the field to empty
                    self.board[i][j] = '_'
        return (maxv, x, y)

    def min(self, alpha, beta):

        # minV values:
        # -1 - win
        # 0  - a tie
        # 1  - loss

        # 2 is worse than the worst case (worst case is 1):
        minv = 2

        x = None
        y = None

        result = self.get_eventual_winner()

        fictiveCoordinate = -1
        if result == 'X':
            return (-1, fictiveCoordinate, fictiveCoordinate)
        elif result == 'O':
            return (1, fictiveCoordinate, fictiveCoordinate)
        elif result == '_':
            return (0, fictiveCoordinate, fictiveCoordinate)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[i][j] == '_':
                    self.board[i][j] = 'X'
                    (v, _, _) = self.max(alpha, beta)
                    if v < minv:
                        minv = v
                        x = i
                        y = j
                    
                    if v <= alpha:
                        # get back the move
                        self.board[i][j] = '_'
                        return (v, x, y)
                    
                    beta = min(beta, v)
                    # get back the move
                    self.board[i][j] = '_'

        return (minv, x, y)

    def is_game_ended(self, result):
        return result != None

    def play(self):
        while True:
            self.display_board()
            self.result = self.get_eventual_winner()

            # Printing the appropriate message if the game has ended
            if self.is_game_ended(self.result):
                if self.result == 'X':
                    print('The tic tac toe winner is X!')
                elif self.result == 'O':
                    print('The tic tac toe winner is O!')
                elif self.result == '_':
                    print("Game is equal!")

                return

            # If it's human's turn
            if self.player_turn == self.human:

                while True:

                    # TODO if self.human == 'X' -> self.min() else self.max()
                    if self.human == 'X':
                        (m, qx, qy) = self.min(-2, 2)
                    else:
                        (m, qx, qy) = self.max(-2, 2)
                    
                    print('Recommended move: x = {}, y = {}'.format(qx, qy))

                    px = int(input('Insert the x coordinate: '))
                    py = int(input('Insert the y coordinate: '))

                    (qx, qy) = (px, py)

                    if self.is_valid(px, py):
                        self.board[px][py] = self.human
                        self.player_turn = self.computer
                        break
                    else:
                        print('The move is not valid! Try again.')

            # If it's computer's turn
            else:
                if self.computer == 'O':
                    (m, px, py) = self.max(-2, 2)
                else:
                    (m, px, py) = self.min(-2, 2)
                
                self.board[px][py] = self.computer
                self.player_turn = self.human
