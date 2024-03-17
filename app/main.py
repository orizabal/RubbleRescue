from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from dao import DaoFactory

# eventlet.monkey_patch()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
CORS(app, resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, debug=False, cors_allowed_origins='*')

"""
Routes:
- update a victim row
"""
victimDao = DaoFactory.createAudioItemDao()

# define WebSocket events that the frontend can subscribe to
@socketio.on('connect')
def handleConnect():
    print(f'Client {request.sid} connected')
    emit('newData', {'newVictim': 2})


@socketio.on('disconnect')
def handleDisconnect():
    print('Client disconnected')


@socketio.on('updateVictim')
def updateVictim(data):
    d = data['victim']['id']
    print(f'Updating victim {d}')
    # victimDao.update(victim)


if __name__ == '__main__':
    socketio.run(app=app)
    # app.run()
