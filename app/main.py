from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from modules import ModuleEventSource
from filter import ModuleSubject
from triangulation import FilterSubject
from dao import DaoFactory
from metrics import Metrics

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
CORS(app, resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, debug=False, cors_allowed_origins='*')
daoFactory = DaoFactory()
metrics = Metrics("e2e")

# define WebSocket events that the frontend can subscribe to
@socketio.on('connect')
def handleConnect():
    print(f'Client {request.sid} connected')
    emitVictims()
    emitModules()


@socketio.on('disconnect')
def handleDisconnect():
    print('Client disconnected')


@socketio.on('updateVictim')
def updateVictim(data):
    d = data['victim']['id']
    print(f'Updating victim {d}')


@socketio.on('deleteVictim')
def deleteVictim(data):
    print(data)


def main():
    moduleEventSource = ModuleEventSource
    moduleSubject = ModuleSubject()
    filterSubject = FilterSubject()

    # Need to add subscribe behaviour before events are re-emitted from the filter
    moduleSubject.subscribe(
        on_next = lambda audioItems: filterSubject.on_next(audioItems),
        on_error = lambda e: filterSubject.on_error(e),
        on_completed = lambda: filterSubject.on_completed()
    )

    # # On subscription, produce_events() is called
    moduleEventSource.subscribe(
        on_next = lambda audioItems: moduleSubject.on_next(audioItems),
        on_error = lambda e: moduleSubject.on_error(e),
        on_completed = lambda: moduleSubject.on_completed()
    )

def emitVictims():
    victimDao = daoFactory.createVictimDao()
    dbVictims = victimDao.get_all()
    victims = []
    for v in dbVictims:
        victims.append({
            'victimId': v[0],
            'coordinates': f'{v[1]}, {v[2]}',
            'foundAt': v[5],
            'truePositive': bool(v[3])
        })

    socketio.emit('newVictims', {'victims': victims})


def emitModules():
    modulesDao = daoFactory.createModuleDao()
    dbModules = modulesDao.get_all()
    modules = []
    for m in dbModules:
        modules.append({
            'id': m[0],
            'coordinates': f'{m[2]}, {m[3]}'
        })
    
    socketio.emit('newModules', {'modules': modules})

socketio.run(app=app)
metrics.trackExecutionTime(main)
