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
    const socket = io('http://127.0.0.1:5000', {
      transports: ['websocket'],
      cors: {
        origin: "http://localhost:3000/"
      }
    });
    setSocketInstance(socket);

    socket.on('connect', (data) => {
      console.log("Connected to server!");
      console.log(data);
    });

    socket.on('connect', (data) => {
      console.log("Disconnected from server.");
      console.log(data);
    });
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
    console.log('Emitting event!!!!!!!')
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
