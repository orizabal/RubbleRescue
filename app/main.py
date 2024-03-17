from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import eventlet
from eventlet import wsgi
from dao import DaoFactory

eventlet.monkey_patch()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
wsgi.server(eventlet.listen(("127.0.0.1", 5000)), app)
CORS(app, resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, debug=False, cors_allowed_origins='*', async_mode='eventlet')

"""
Routes:
- update a victim row
"""
victimDao = DaoFactory.createAudioItemDao()

# define WebSocket events that the frontend can subscribe to
@socketio.on('connect')
def handleConnect():
    print('Client connected')


@socketio.on('disconnect')
def handleDisconnect():
    print('Client disconnected')


@socketio.on('updateVictim')
def updateVictim(victim):
    print("HEREEEEE ============================================================================")
    print(f'Updating victim {victim.id}')
    # victimDao.update(victim)


if __name__ == '__main__':
    socketio.run(app=app)
