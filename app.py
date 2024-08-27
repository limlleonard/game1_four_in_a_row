import pygame as pg
import random
import numpy as np
import time

R = 6  # total number of row
C = 7  # total number of column
W = 4  # number to win
SQ = 80  # size of a square


def count_windows(board, n=4, color=1):
    """n: number in a line, c: color of the player. Count how many windows, which have n pieces of the selected color. A window indicate a row in horizontal, vertical or diagnol direction with a length of W=4"""
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

    def move_both(self, board, _=0):
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

    def move_both(self, _, a1):
        """human doesn't need the board, it just return what he gets"""
        return a1


class Game:
    def __init__(self, a1):
        """Game has two players, p1 and p2."""
        if a1 == 1:
            self.p1 = Human(1)
            self.p2 = Human(2)
        elif a1 == 2:
            self.p1 = Human(1)
            self.p2 = Robot(2)
        elif a1 == 3:
            self.p1 = Robot(1)
            self.p2 = Human(2)
        elif a1 == 4:
            self.p1 = Robot(1)
            self.p2 = Robot(2)
        self.board = np.zeros((R, C), dtype=int)
        self.valid_p1 = self.valid_p2 = self.turn = True  # valid move

    def move_game(self, a1=7):
        """Move controlled by game. If turn is true, p1 is in turn"""
        if self.turn:
            mt = self.p1.move_both(self.board, a1)
            if mt in range(C):
                self.valid_p1 = move1(self.board, mt, self.p1.c)
                self.turn = not self.turn  # only switch, if make a valid move
        else:
            mt = self.p2.move_both(self.board, a1)
            if mt in range(C):
                self.valid_p2 = move1(self.board, mt, self.p2.c)
                self.turn = not self.turn

    def winc(self):
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
            return False


play = True
pg_nr_dict = {
    pg.K_0: 0,
    pg.K_1: 1,
    pg.K_2: 2,
    pg.K_3: 3,
    pg.K_4: 4,
    pg.K_5: 5,
    pg.K_6: 6,
}
start_text1 = "1: human vs human  2: human vs robot"
start_text2 = "3: robot vs human  4: robot vs robot"
clock = pg.time.Clock()
pg.init()
pg.display.set_caption("Four in a row")
screen = pg.display.set_mode((SQ * C, SQ * (R + 1)))
stage = 1
g1 = Game(1)


def draw_board(stage):
    for x in range(C):
        for y in range(R):
            pg.draw.circle(
                screen, "#CDC0B4", (x * SQ + SQ // 2, y * SQ + SQ // 2), SQ // 3, 4
            )
    if stage == 1:
        guide1 = pg.font.SysFont("Arial", 30).render(start_text1, False, (0, 255, 0))
        screen.blit(guide1, (SQ // 4, SQ * R))
        guide1 = pg.font.SysFont("Arial", 30).render(start_text2, False, (0, 255, 0))
        screen.blit(guide1, (SQ // 4, SQ * R + SQ // 2))
    elif stage == 2:
        pass
    elif stage == 3:
        guide1 = pg.font.SysFont("Arial", 30).render(win_tf, False, (0, 255, 0))
        screen.blit(guide1, (SQ // 4, SQ * R))
        guide1 = pg.font.SysFont("Arial", 30).render("Again?(0/1)", False, (0, 255, 0))
        screen.blit(guide1, (SQ // 4, SQ * R + SQ // 2))


def draw_pieces(board):
    for x in range(C):  # Draw board
        for y in range(R):
            if board[y][x] == 1:
                pg.draw.circle(
                    screen,
                    (200, 0, 0),
                    (x * SQ + SQ // 2, y * SQ + SQ // 2),
                    SQ // 3,
                )
            if board[y][x] == 2:
                pg.draw.circle(
                    screen,
                    (0, 200, 200),
                    (x * SQ + SQ // 2, y * SQ + SQ // 2),
                    SQ // 3,
                )


while play:
    clock.tick(40)
    screen.fill((0, 0, 0))
    if stage == 2:
        win_tf = g1.winc()
        if win_tf:
            stage = 3
        else:
            g1.move_game()
    for e in pg.event.get():
        if e.type == pg.QUIT:
            play = False
        if e.type == pg.KEYDOWN and e.key in pg_nr_dict:
            a1 = pg_nr_dict[e.key]
            if stage == 1 and pg_nr_dict[e.key] in range(1, 5):
                g1 = Game(pg_nr_dict[e.key])
                stage = 2
            elif stage == 2:
                g1.move_game(pg_nr_dict[e.key])
            elif stage == 3:
                if pg_nr_dict[e.key] == 0:
                    play = False
                elif pg_nr_dict[e.key] == 1:
                    stage = 1
        elif e.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
            if stage == 2:
                mx, my = pg.mouse.get_pos()
                g1.move_game(mx // SQ)
            pass
    draw_board(stage)
    if stage > 1:  # shows result even it is finished
        draw_pieces(g1.board)
    pg.display.flip()
