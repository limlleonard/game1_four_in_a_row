import random
import numpy as np
from queue import Queue
import time

R = 6  # total number of row
C = 7  # total number of column
W = 4  # number to win
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

def count_windows(board, n=4, color=1) -> int:
    """n: number in a line, color: color of the player. The function counts how many windows, which have n pieces of the selected color. A window indicates a row in horizontal, vertical or diagnol direction with a length of W=4"""
    counter = 0

    def check_window(l4: int) -> int:
        """if there are n pieces of the selected color in the window and the rest is empty"""
        return list(l4).count(color) == n and list(l4).count(0) == W - n

    for k1 in range(R):  # win horizontal
        for k2 in range(C - W + 1):
            if check_window(board[k1, k2 : k2 + W]):
                counter += 1
    for k1 in range(R - W + 1):  # win vertical
        for k2 in range(C):
            if check_window(board[k1 : k1 + W, k2]):
                counter += 1
    for k1 in range(R - W + 1):  # diagnol
        for k2 in range(C - W + 1):
            lt1 = []  # list temp 1
            lt2 = []
            for k3 in range(W):
                lt1.append(board[k1 + k3, k2 + k3])
                lt2.append(board[k1 + W - k3 - 1, k2 + k3])
            if check_window(lt1):
                counter += 1
            if check_window(lt2):
                counter += 1
    return counter

class Game:
    def __init__(self):
        self.letzt_pos=None
        # self.reset()
        self.board = np.zeros((R, C), dtype=int)
        self.turn=True

        self.r1=Robot(True)
        self.r2=Robot(False)

    def reset(self):
        self.board = np.zeros((R, C), dtype=int)
        self.turn = True  # valid move

    def move(self, pos: int) -> bool:
        """Drop a piece of the color to position, return true of false if the move is success (in case the column is already full). It checks from the bottom row, if it is empty, then places the piece where the first empty row appears"""
        color=1 if self.turn else 2
        for k1 in range(R):
            if not self.board[R - k1 - 1][pos]:
                self.board[R - k1 - 1][pos] = color
                self.turn=not self.turn
                self.letzt_pos=(R - k1 - 1, pos)
                return True
        return False
    
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

    def win_check(self):
        # player who played the last move
        last_player=2 if self.turn else 1
        r1 = count_windows(self.board, W, last_player)
        if r1 > 0:
            return f"P{last_player} wins"
        elif np.count_nonzero(self.board == 0) == 0:
            return "Tie"
        else:
            return ""
        
    def gloop(self, p1, p2, socketio, q1):
        message=''
        while True: # loop of game
            # get a input from player 1
            pos1=pos2=''
            if p1=='h':
                pos1=q1.get()
            elif p1=='r':
                pos1=self.r1.choose_pos(self.board)
            else:
                break
            if pos1==9:
                break
            legal=self.move(pos1)
            if not legal:
                message='Player 1 played illegal move, player 2 wins'
                break
            self.draw()
            socketio.emit('drop_info', {'pos1':self.letzt_pos, 'turn':self.turn})
            message=self.win_check()
            if len(message):
                break
            time.sleep(1)
            # player 2
            if p2=='h':
                pos2=q1.get()
            elif p2=='r':
                pos2=self.r2.choose_pos(self.board)
            else:
                break
            if pos2==9:
                break
            legal=self.move(pos2)
            if not legal:
                message='Player 2 played illegal move, player 1 wins'
                break
            self.draw()
            socketio.emit('drop_info', {'pos1':self.letzt_pos, 'turn':self.turn})
            message=self.win_check()
            if len(message):
                break
            time.sleep(1)
        socketio.emit('drop_info', {'message':message})

class Robot:
    def __init__(self, p1=True):
        # if it is player1
        self.p1=p1

    def reverse_board(self, board):
        """robot should think he is always player 1. If he is player 2 infact, the board sent to him should be reversed"""
        board1=board.copy()
        for row in range(R):
            for col in range(C):
                if board1[row][col]>0:
                    board1[row][col]=board1[row][col]%2+1
        return board1
    
    def move_fantacy(self, board, pos: int, color: int) -> bool:
        """make a fantacy move to calculate score of the opponent"""
        for k1 in range(R):
            if not board[R - k1 - 1][pos]:
                board[R - k1 - 1][pos] = color
                return True
        return False
    
    def score1(self, board, i, c):
        """Score represent how important a position is for robot itself and the opponent.
        Score is calculated by how many 4,3,2 pieces in a window when itself or the opponent play to position i"""
        board_temp = board.copy()
        self.move_fantacy(board_temp, i, c)
        i4 = count_windows(board_temp, 4, c)  # play in i would get i4 4 in a row
        i3 = count_windows(board_temp, 3, c)
        i2 = count_windows(board_temp, 2, c)
        board_temp = board.copy()
        self.move_fantacy(board_temp, i, c % 2 + 1)  # fantacy move by opponent
        y4 = count_windows(board_temp, 4, c % 2 + 1)
        y3 = count_windows(board_temp, 3, c % 2 + 1)
        y2 = count_windows(board_temp, 2, c % 2 + 1)
        return i4 * 10**4 + y4 * 10**3 + i3 * 10**2 + y3 * 10 + i2 * 5 + y2 * 2

    def scores(self, board, c) -> dict:
        """Calculate the scores of all the poisitions and return them as a dictionary"""
        dict1 = {}
        for i in range(C):
            if board[0][i] == 0: # if there is place to play
                dict1[i] = self.score1(board, i, c)
        return dict1

    def choose_pos(self, board):
        if self.p1:
            board1=board.copy()
        else:
            board1=self.reverse_board(board)
        dict1 = self.scores(board1, 1)
        print(dict1)
        if len(dict1)==1:
            for pos1 in dict1:
                return pos1
        for k in dict1:
            board2 = board1.copy()
            self.move_fantacy(board2, k, 1)  # make fantacy move myself, to calculate opponent
            dict2 = self.scores(board2, 2)
            dict1[k] -= max(dict2.values()) // 2
        print(dict1)
        if -5 < max(dict1.values()) < 5:
            pos1= random.randint(0, C - 1)
        else:
            pos1=max(dict1, key=dict1.get)
        return pos1
