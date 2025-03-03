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
    app.config['game_on']=True
    while not app.config['queue'].empty():
        app.config['queue'].get()
    g1=Game()
    p1, p2=mode
    app.config['thread']=Thread(target=g1.gloop,
                                args=(p1,p2, socketio, app.config['queue']))
    app.config['thread'].start()
    return '', 204

@app.route("/reset", methods=["POST"])
def reset():
    """queue hat ein bestimmtes Typ, deshalb put('q') funktioniert nicht, weil 'q' ist ein string typ
    Ich vermute, wenn queue ist zum Erstmal eingefügt wird, wird der typ bestimmt"""
    app.config['queue'].put(9)
    app.config['game_on']=False
    return '', 204

@app.route("/klicken", methods=["POST"])
def klicken():
    if app.config['game_on']:
        pos1=request.json.get('pos1')
        app.config['queue'].put(pos1)
    return '', 204

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001, host="0.0.0.0", allow_unsafe_werkzeug=True)
    # app.run(debug=True, port=5001, host="0.0.0.0")
