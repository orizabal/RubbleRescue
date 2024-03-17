import { useCallback, useEffect, useState } from 'react';
import io from 'socket.io-client';
import './App.css';
import DeleteVictimPopUp from './components/deleteVictim/DeleteVictimPopUp';
import SidePanel from './components/hoc/sidePanel/SidePanel';
import MapComponent from './components/hoc/map/MapComponent';

function App() {
  // const socket = socketIOClient('http://127.0.0.1:5000');
  const [socketInstance, setSocketInstance] = useState(null);
  useEffect(() => {
    const socket = io('127.0.0.1:5000', {
      transports: ['websocket'],
      cors: {
        origin: "http://localhost:3000/"
      }
    });

    setSocketInstance(socket);

    socket.on('connect', () => {
      console.log("Client is connected to server!");
    });

    socket.on('disconnect', () => {
      console.log("Client is disconnected from server.");
    });

    socket.on('newData', (data) => {
      console.log('New data from server: ' + data['newVictim']);
    })
  }, []);

  const [selectedVictim, setSelectedVictim] = useState(null);
  const [victimToDelete, setVictimToDelete] = useState(null);

  function handleSelectListItem(victim) {
    setSelectedVictim(victim);
  }

  function handleSelectDelete(e, victim) {
    e.stopPropagation();
    setVictimToDelete(victim);
  }

  function closeVictimPopUp() {
    setSelectedVictim(null);
  }

  function closeDeletePopUp() {
    console.log(socketInstance.emit('updateVictim', {
      victim: {
        id: 1
      }
    }));
    setVictimToDelete(null);
  }

  return (
    <div className="App">
      <SidePanel onDelete={handleSelectDelete} onSelect={handleSelectListItem} selectedVictim={selectedVictim} />
      <MapComponent selectedVictim={selectedVictim} onCloseVictimInfo={closeVictimPopUp} />
      {victimToDelete &&
        <DeleteVictimPopUp
          victimId={victimToDelete.victimId}
          coordinates={victimToDelete.coordinates}
          foundAt={victimToDelete.foundAt}
          onClose={closeDeletePopUp}
          onCancel={closeDeletePopUp}
          onConfirm={closeDeletePopUp}
        />
      }
    </div>
  );
}

export default App;
