from model import *

str_start = """
Choose mode of the game and press 'Enter':
1: human vs human  2: human vs robot
3: robot vs human  4: robot vs robot
q: quit
"""
str_play = """
Press the correspondent number key to drop the piece.
Press 'q' to quit.
"""
str_again = "Once again? (1/0)\n"
stage = 1
g1 = None

turn2nr = lambda x: 1 if x else 2


def get_pos():
    while True:
        pos = input(str_play)
        if pos == "q":
            return "q"
        try:
            pos = int(pos)
            if pos in range(C):
                return pos
        except:
            pass


while stage < 4:
    while stage == 1:
        mode = input(str_start)
        if mode == "q":
            stage = 4
            break
        try:
            mode = int(mode)
            if mode in range(1, 5):
                stage = 2
        except:
            pass
    while stage == 2:
        if g1 is None:
            g1 = Game(mode)
        win_control = g1.winc()
        if len(win_control) == 0:
            g1.draw()
            if g1.turn:
                if type(g1.p1) is Robot:
                    pos = g1.p1.move_player(g1.board)
                else:
                    pos = get_pos()
            else:
                if type(g1.p2) is Robot:
                    pos = g1.p2.move_player(g1.board)
                else:
                    pos = get_pos()
            if pos == "q":
                stage = 4
            else:
                g1.add_to_board(pos, turn2nr(g1.turn))
                g1.turn = not g1.turn

            # nachteil: muss jedes mal kontrollieren, p1 ist Robot oder Mensch
        else:
            g1.draw()
            print(win_control + "\n")
            stage = 3
    while stage == 3:
        again = input(str_again)
        if again == "1":
            stage = 1
        elif again == "0":
            stage = 4
