import pygame as pg
from model import *

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
            nr = pg_nr_dict[e.key]
            if stage == 1 and nr in range(1, 5):
                g1 = Game(nr)
                stage = 2
            elif stage == 2:
                g1.move_game(nr)
            elif stage == 3:
                if nr == 0:
                    play = False
                elif nr == 1:
                    stage = 1
        elif e.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
            if stage == 2:
                mx, my = pg.mouse.get_pos()
                g1.move_game(mx // SQ)
    draw_board(stage)
    if stage > 1:  # shows result even it is finished
        draw_pieces(g1.board)
    pg.display.flip()
