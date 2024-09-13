import random
import numpy as np

R = 6  # total number of row
C = 7  # total number of column
W = 4  # number to win
SQ = 80  # size of a square


def count_windows(board, n=4, color=1):
    """n: number in a line, color: color of the player. The function counts how many windows, which have n pieces of the selected color. A window indicates a row in horizontal, vertical or diagnol direction with a length of W=4"""
    counter = 0

    def cw(l4):
        """Check window, if there are n pieces of the selected color in the window and the rest is empty"""
        return list(l4).count(color) == n and list(l4).count(0) == W - n

    for k1 in range(R):  # win horizontal
        for k2 in range(C - W + 1):
            if cw(board[k1, k2 : k2 + W]):
                counter += 1
    for k1 in range(R - W + 1):  # win vertical
        for k2 in range(C):
            if cw(board[k1 : k1 + W, k2]):
                counter += 1
    for k1 in range(R - W + 1):  # diagnol
        for k2 in range(C - W + 1):
            lt1 = []  # list temp 1
            lt2 = []
            for k3 in range(W):
                lt1.append(board[k1 + k3, k2 + k3])
                lt2.append(board[k1 + W - k3 - 1, k2 + k3])
            if cw(lt1):
                counter += 1
            if cw(lt2):
                counter += 1
    return counter


def move1(board, pos, color):
    """Drop a piece of the color to position, return true of false if the move is success (in case the column is already full). It checks from the bottom row, if it is empty, then places the piece where the first empty row appears"""
    for k1 in range(R):
        if not board[R - k1 - 1][pos]:
            board[R - k1 - 1][pos] = color
            return True
    return False


class Robot:
    def __init__(self, c):
        self.c = c  # color
        # self.board = []
        # self.mp = []

    def score1(self, board, i, c):
        """Score is calculated by how many 4,3,2 pieces in a window."""
        lt = board.copy()
        move1(lt, i, c)
        i4 = count_windows(lt, 4, c)  # i would get a 4
        i3 = count_windows(lt, 3, c)
        i2 = count_windows(lt, 2, c)
        lt = board.copy()
        move1(lt, i, c % 2 + 1)  # fantacy move by opponent
        y4 = count_windows(lt, 4, c % 2 + 1)
        y3 = count_windows(lt, 3, c % 2 + 1)
        y2 = count_windows(lt, 2, c % 2 + 1)
        return i4 * 10**4 + y4 * 10**3 + i3 * 10**2 + y3 * 10 + i2 * 5 + y2 * 2

    def scores(self, board, c) -> dict:
        """Calculate the scores of all the poisitions and return them as a dictionary"""
        dict1 = {}
        for i in range(C):
            if board[0][i] == 0:
                dict1[i] = self.score1(board, i, c)
        return dict1

    def move_player(self, board, _=0):
        """the second parameter is not needed here, but human mover need this"""
        dict1 = self.scores(board.copy(), self.c)
        print(dict1)
        for k in dict1:
            l2 = board.copy()
            move1(l2, k, self.c)  # make fantacy move myself, to calculate opponent
            dict2 = self.scores(l2, self.c % 2 + 1)
            dict1[k] -= max(dict2.values()) // 2
        print(dict1)
        if -5 < max(dict1.values()) < 5:
            return random.randint(0, C - 1)
        return max(dict1, key=dict1.get)


class Human:
    def __init__(self, c):
        self.c = c

    def move_player(self, _, a1):
        """human doesn't need the board, it just return what he gets"""
        return a1


class Game:
    def __init__(self, mode):
        """Game has two players, p1 and p2. Board is a 2d np array, top row is row0. By default, moves from p1 and p2 are true. turn=true means p1 is in turn"""
        # dct_human_robot={1:}
        if mode == 1:
            self.p1 = Human(1)
            self.p2 = Human(2)
        elif mode == 2:
            self.p1 = Human(1)
            self.p2 = Robot(2)
        elif mode == 3:
            self.p1 = Robot(1)
            self.p2 = Human(2)
        elif mode == 4:
            self.p1 = Robot(1)
            self.p2 = Robot(2)
        self.board = np.zeros((R, C), dtype=int)
        self.valid_p1 = self.valid_p2 = self.turn = True  # valid move

    def add_to_board(self, pos, color):
        return move1(self.board, pos, color)

    def move_game(self, a1=7):
        """Move controlled by game. If turn is true, p1 is in turn. With the default parameter, it is an invalid move"""
        if self.turn:
            mt = self.p1.move_player(self.board, a1)
            if mt in range(C):
                self.valid_p1 = move1(self.board, mt, self.p1.c)
                self.turn = not self.turn  # only switch, if make a valid move
                self.draw()
        else:
            mt = self.p2.move_player(self.board, a1)
            if mt in range(C):
                self.valid_p2 = move1(self.board, mt, self.p2.c)
                self.turn = not self.turn
                self.draw()
        if a1 != 7:
            pass

    def move_until_human(self, a1=7):
        """Keep moving until human input is needed"""
        done = False
        if not done:
            if self.turn:
                mt = self.p1.move_player(self.board, a1)
                if mt in range(C):
                    self.valid_p1 = move1(self.board, mt, self.p1.c)
                    self.turn = not self.turn  # only switch, if make a valid move
                    self.draw()
            else:
                mt = self.p2.move_player(self.board, a1)
                if mt in range(C):
                    self.valid_p2 = move1(self.board, mt, self.p2.c)
                    self.turn = not self.turn
                    self.draw()
            if (
                (type(self.p1) is Human and self.turn)
                or (type(self.p2) is Human and not self.turn)
                or (self.winc())
            ):
                done = True

    def winc(self):
        """Win control"""
        r1 = count_windows(self.board, W, 1)
        r2 = count_windows(self.board, W, 2)
        # time.sleep(1)
        if r1 > 0 or not self.valid_p2:
            print(r1)
            print(self.valid_p2)
            return "P1 wins"
        elif r2 > 0 or not self.valid_p1:
            print(r2)
            print(self.valid_p1)
            return "P2 wins"
        elif np.count_nonzero(self.board == 0) == 0:
            return "Tie"
        else:
            return ""

    def draw(self):
        """Draw the board and pieces in Terminal"""
        dct_draw = {0: "_", 1: "X", 2: "O"}
        str1 = ""
        for r1 in range(R):
            for c1 in range(C):
                str1 += dct_draw[self.board[r1][c1]]
                if c1 < C - 1:
                    str1 += "|"
            str1 += "\n"
        for c1 in range(C):
            str1 += str(c1)
            if c1 < C - 1:
                str1 += "|"
        print(str1)
