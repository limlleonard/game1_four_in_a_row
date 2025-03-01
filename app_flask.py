from game import Game, Robot, C
from app_terminal import translate_mode
import time
import random
from threading import Thread, Event
from queue import Queue

from flask import Flask, request, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

app.config['game_on']=False
app.config['event']=Event()
app.config['queue']=Queue()

@app.route("/", methods=["GET"])
def index():
    """return home page"""
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    """start playing game"""
    mode=request.json.get('mode') # mögliche mode: hh, hr, rh, rr
    app.config['g1']=Game()
    app.config['r1']=Robot(True)
    app.config['r2']=Robot(False) # doesn't have to be used
    p1, p2=mode
    app.config['thread']=Thread(target=game_loop, 
                                args=(app.config['g1'], app.config['r1'], app.config['r2'], p1,p2))
    app.config['thread'].start()
    app.config['game_on']=True
    return '', 204

@app.route("/klicken", methods=["POST"])
def klicken():
    if app.config['game_on']:
        pos1=request.json.get('pos1')
        app.config['queue'].put(pos1)
    return '', 204

def game_loop(g1, r1, r2, p1, p2):
    message=''
    while True: # loop of game
        # get a input from player 1
        if p1=='h':
            pos1=app.config['queue'].get()
        elif p1=='r':
            pos1=r1.choose_pos(g1.board)
        else:
            break
        if pos1=='q':
            break
        legal=g1.move(pos1)
        if not legal:
            message='Player 1 played illegal move, player 2 wins'
            break
        g1.draw()
        socketio.emit('drop_info', {'pos1':g1.letzt_pos, 'turn':g1.turn})
        message=g1.win_check()
        if len(message):
            break
        time.sleep(1)
        # player 2
        if p2=='h':
            pos1=app.config['queue'].get()
        elif p2=='r':
            pos1=r2.choose_pos(g1.board)
        if pos1=='q':
            break
        legal=g1.move(pos1)
        if not legal:
            message='Player 2 played illegal move, player 1 wins'
            break
        g1.draw()
        socketio.emit('drop_info', {'pos1':g1.letzt_pos, 'turn':g1.turn})
        message=g1.win_check()
        if len(message):
            break
        time.sleep(1)
    app.config['game_on']=False
    socketio.emit('drop_info', {'message':message})
    # print(message)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001, host="0.0.0.0", allow_unsafe_werkzeug=True)
    # app.run(debug=True, port=5001, host="0.0.0.0")
