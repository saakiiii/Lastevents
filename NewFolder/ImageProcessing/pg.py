from datetime import datetime
from distutils.log import debug
from flask import *
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def send():
    return render_template("chatspace.html")

@socketio.on('connect')
def connect(data):
    print(data)
    socketio.send({"result":"connected"})

@socketio.on('message')
def message(data):
    print(data)
    socketio.send(data)

if __name__ == "__main__":
 socketio.run(app, debug=True)