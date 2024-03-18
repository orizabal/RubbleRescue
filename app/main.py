import os
import sys, time
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
    emit('newVictims', {'victims': [
        {
            'victimId': 1,
            'coordinates': "12.3422, 52.1232",
            'foundAt': "15:31:02",
            'truePositive': False
        },
        {
            'victimId': 2,
            'coordinates': "50.3422, 52.1232",
            'foundAt': "16:31:02",
            'truePositive': False
        },
        {
            'victimId': 3,
            'coordinates': "24.3422, 30.1232",
            'foundAt': "05:00:02",
            'truePositive': False
        },
        {
            'victimId': 4,
            'coordinates': "15.3422, 60.1232",
            'foundAt': "09:21:55",
            'truePositive': False
        },
        {
            'victimId': 5,
            'coordinates': "38.3422, 10.1232",
            'foundAt': "00:45:02",
            'truePositive': False
        }]
    })
    emit('newModules', {'modules': [
        {
            'id': 1,
            'coordinates': "60.3422, 12.1232"
        },
        {
            'id': 2,
            'coordinates': "20.3422, 70.1232"
        },
        {
            'id': 3,
            'coordinates': "45.3422, 40.1232"
        }]
    })


@socketio.on('disconnect')
def handleDisconnect():
    print('Client disconnected')


@socketio.on('updateVictim')
def updateVictim(data):
    d = data['victim']['id']
    print(f'Updating victim {d}')
    # victimDao.update(victim)

@socketio.on('deleteVictim')
def deleteVictim(data):
    print(data)
    # victimId = data['victimId']
    # truePositive = data['truePositive']
    # locationChecked = data['locationChecked']

    # print(f'vi: {victimId}, tp: {truePositive}, lc: {locationChecked}')'


if __name__ == '__main__':
    socketio.run(app=app)
    # app.run()
