from game import Robot, Human, Game, C
import time

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
first_time = True

turn2nr = lambda x: 1 if x else 2


def get_pos(first_time=True):
    while True:
        if first_time:
            pos = input(str_play)
        else:
            pos = input()
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
        g1.draw()
        if len(win_control) == 0:
            current_player = g1.p1 if g1.turn else g1.p2
            if isinstance(current_player, Robot):
                pos = current_player.move_player(g1.board)
                time.sleep(1)
            else:
                pos = get_pos(first_time)
                first_time = False
            if pos == "q":
                stage = 4
            else:
                g1.add_to_board(pos, turn2nr(g1.turn))
                g1.turn = not g1.turn
        else:
            print(win_control + "\n")
            stage = 3
    while stage == 3:
        again = input(str_again)
        if again == "1":
            stage = 1
            g1 = None
        elif again == "0":
            stage = 4
