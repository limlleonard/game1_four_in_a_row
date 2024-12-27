from game import Game, Robot, C
import time
import random
str_start = """
Choose mode of the game and press 'Enter':
1: human vs human  2: human vs robot (human first)
3: robot vs human  4: robot vs robot
q: quit
"""
str_play = """
Press the correspondent number key to drop the piece.
Press 'q' to quit.
"""
str_again = "Once again? (1/0)\n"
def choose_mode():
    while True: # choose mode
        mode = input(str_start)
        if mode == "q":
            return "q"
        try:
            mode = int(mode)
            if mode in range(1, 5):
                return mode
        except:
            pass
def translate_mode(mode):
    if mode == 1:
        return 'hh'
    elif mode == 2:
        return 'hr'
    elif mode == 3:
        return 'rh'
    elif mode == 4:
        return 'rr'
def choose_pos(first_time: bool = False):
    """Get the input from the user. It is used to get the mode of the game when it is played for the first time or for the position of the next piece to play"""
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

def game_loop(g1, r1, r2, p1, p2):
    message=''
    while True: # loop of game
        # get a input from player 1
        if p1=='h':
            pos1=choose_pos()
        elif p1=='r':
            pos1=r1.choose_pos(g1.board)
        if pos1=='q':
            break
        legal=g1.move(pos1)
        if not legal:
            message='Player 1 played illegal move, player 2 wins'
            break
        g1.draw()
        message=g1.win_check()
        if len(message):
            break
        # player 2
        if p2=='h':
            pos1=choose_pos()
        elif p2=='r':
            pos1=r2.choose_pos(g1.board)
        if pos1=='q':
            break
        legal=g1.move(pos1)
        if not legal:
            message='Player 2 played illegal move, player 1 wins'
            break
        g1.draw()
        message=g1.win_check()
        if len(message):
            break
        time.sleep(1)
    return message

def play():
    while True: # loop of choose mode
        mode=choose_mode()
        if mode=="q":
            break
        else:
            g1=Game()
            g1.draw()
            r1=Robot(True)
            r2=Robot(False) # doesn't have to be used
            p1,p2=translate_mode(mode)
            message=game_loop(g1,r1,r2,p1,p2)
            print(message)
            # continue?
            again = input(str_again)
            if again == "1":
                continue
            elif again == "0":
                break

if __name__ == "__main__":
    play()
    # start(stage)