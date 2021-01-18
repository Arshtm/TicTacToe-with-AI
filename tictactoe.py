import random


class TicTacToe:
    name = 'Tic-Tac-Toe'
    states = ['start', 'exit']
    players = ['user', 'easy', 'medium', 'hard']
    x, o = 'X', 'O'

    def __init__(self):
        self.first_player = None
        self.second_player = None
        self.game_state = None
        self.o_x = None

    def beginning(self):
        while True:
            parameters = input('Input command: ').split()
            if parameters[0] == self.states[1]:
                break
            if (len(parameters) != 3 or parameters[0] not in self.states or parameters[1] not in self.players
                    or parameters[2] not in self.players):
                print("Bad parameters")
            else:
                self.game_state = parameters[0]
                self.first_player = parameters[1]
                self.second_player = parameters[2]
                self.o_x = list(' ' * 9)
                self.main_body()

    def main_body(self):
        self.field_print()
        while True:
            self.move(self.first_player, self.x)
            self.field_print()
            result = self.result()
            if result == 'Draw':
                print('Draw')
                break
            elif result in self.o_x:
                print(f'{result} wins\n')
                break
            else:
                pass
            self.move(self.second_player, self.o)
            self.field_print()
            result = self.result()
            if result == 'Draw':
                print('Draw')
                break
            elif result in self.o_x:
                print(f'{result} wins\n')
                break
            else:
                pass

    def move(self, who, symbol):
        if who == self.players[0]:  # player
            self.user_move(symbol)
        if who == self.players[1]:  # easy
            self.easy_move(symbol)
        if who == self.players[2]:  # medium
            self.medium_move(symbol)
        if who == self.players[3]:  # medium
            self.hard_move(symbol)

    def field_print(self):
        print('-' * 9)
        for i in [0, 3, 6]:                          # printing three single rows
            print('| {0} {1} {2} |'.format(self.o_x[i], self.o_x[i + 1], self.o_x[i + 2]))
        print('-' * 9)

    def user_move(self, letter):
        matrix = []
        for k in [0, 3, 6]:
            matrix.append([self.o_x[k], self.o_x[k + 1], self.o_x[k + 2]])
        while True:
            coordinates = input('Enter the coordinates: ')
            if coordinates[0].isdigit():
                x, y = map(int, coordinates.split())
                if x in [1, 2, 3] and y in [1, 2, 3]:
                    if matrix[-y][x-1] == ' ':
                        self.o_x[x - 3 * y + 8] = letter
                        break
                    else:
                        print("This cell is occupied! Choose another one!")
                else:
                    print("Coordinates should be from 1 to 3!")
            else:
                print('You should enter numbers!')

    def easy_move(self, letter):
        empty = self.empty()
        comp_coord = random.choice(empty)
        self.o_x[comp_coord] = letter
        print('Making move level "easy"')

    def medium_move(self, letter):
        if letter == self.o:
            letter2 = self.x
        else:
            letter2 = self.o
        key = None
        try:
            x, y = self.can_finish_line(letter)
            self.o_x[3 * x + y] = letter
            key = True
        except Exception:
            pass
        if key is not True:
            try:
                x, y = self.can_finish_line(letter2)
                self.o_x[3 * x + y] = letter
                key = True
            except Exception:
                pass
        if key is not True:
            empty = self.empty()
            comp_coord = random.choice(empty)
            self.o_x[comp_coord] = letter
        print('Making move level "medium"')

    def can_finish_line(self, player):
        matrix = []
        for k in [0, 3, 6]:
            matrix.append([self.o_x[k], self.o_x[k + 1], self.o_x[k + 2]])
        for i in range(3):
            if matrix[i].count(player) == 2:
                try:
                    return i, matrix[i].index(' ')
                except ValueError:
                    pass
            if (slice_ := [matrix[j][i] for j in range(3)]).count(player) == 2:
                try:
                    return slice_.index(' '), i
                except ValueError:
                    pass
        if (slice_ := [matrix[i][i] for i in range(3)]).count(player) == 2:
            try:
                free = slice_.index(' ')
                return free, free
            except ValueError:
                pass
        if (slice_ := [matrix[i][2 - i] for i in range(3)]).count(player) == 2:
            try:
                free = slice_.index(' ')
                return free, 2 - free
            except ValueError:
                pass
        return None

    def result(self):
        for i in [0, 3, 6]:
            if self.o_x[i] == self.o_x[i+1] == self.o_x[i+2] and self.o_x[i] in ['X', 'O']:  # checking not empty rows
                return self.o_x[i]
            if self.o_x[i // 3] == self.o_x[i // 3 + 3] == self.o_x[i // 3 + 6] and self.o_x[i // 3] in ['X', 'O']:
                return self.o_x[i // 3]
        else:
            if (self.o_x[0] == self.o_x[4] == self.o_x[8] or self.o_x[2] == self.o_x[4] == self.o_x[6]) and self.o_x[4] in ['X', 'O']:
                return self.o_x[4]  # checking not empty diagonals (upper line)
            elif ' ' not in self.o_x:
                return 'Draw'
            else:
                return True

    def hard_move(self, letter):
        score, best_move = self.minimax(self.o_x, letter)
        self.o_x[best_move] = letter
        print('Making move level "hard"')

    def minimax(self, grid, symbol):
        result = self.result()
        if result == self.o or result == self.x:
            return (1 if symbol == self.o else -1), None
        elif result == 'Draw':
            return 0, None
        elif symbol is self.x:
            best_score = -2
            best_move = None
            for move in self.empty():
                grid[move] = symbol
                score, mv = self.minimax(self.o_x, self.o)
                grid[move] = ' '
                if score >= best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        elif symbol is self.o:
            best_score = 2
            best_move = None
            for move in self.empty():
                grid[move] = symbol
                score, mv = self.minimax(self.o_x, self.x)
                grid[move] = ' '
                if score <= best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move

    def empty(self):
        empty = []
        for i in range(9):
            if self.o_x[i] == ' ':
                empty.append(i)
        return empty


game = TicTacToe()
game.beginning()
