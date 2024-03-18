import { useEffect, useState } from 'react';
import io from 'socket.io-client';
import './App.css';
import DeleteVictimPopUp from './components/deleteVictim/DeleteVictimPopUp';
import SidePanel from './components/hoc/sidePanel/SidePanel';
import MapComponent from './components/hoc/map/MapComponent';

function App() {
  const [selectedVictim, setSelectedVictim] = useState(null);
  const [victimToDelete, setVictimToDelete] = useState(null);
  const [victims, setVictims] = useState([]);
  const [rescuedVictims, setRescuedVictims] = useState([]);
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

    socket.on('newVictims', (data) => {
      console.log('New victims detected.');
      setVictims([...victims, ...data['victims']]);
    });
  }, []);

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
    setVictimToDelete(null);
  }

  function confirmDelete() {
    socketInstance.emit('deleteVictim',
    {
      victimId: victimToDelete.victimId,
      truePositive: victimToDelete.truePositive,
      locationChecked: true
    });

    let indexToRemove = victims.indexOf(victimToDelete);
    if (indexToRemove > -1) {
      setVictims(victims.filter((v) => {return v !== victimToDelete}));
    }

    if (victimToDelete.truePositive) {
      setRescuedVictims([...rescuedVictims, victimToDelete]);
    }
    closeDeletePopUp();
  }

  return (
    <div className="App">
      <SidePanel onDelete={handleSelectDelete} onSelect={handleSelectListItem} selectedVictim={selectedVictim} victimsList={victims} />
      <MapComponent selectedVictim={selectedVictim} onCloseVictimInfo={closeVictimPopUp} />
      {victimToDelete &&
        <DeleteVictimPopUp
          victimId={victimToDelete.victimId}
          coordinates={victimToDelete.coordinates}
          foundAt={victimToDelete.foundAt}
          onClose={closeDeletePopUp}
          onCancel={closeDeletePopUp}
          onConfirm={confirmDelete}
        />
      }
    </div>
  );
}

export default App;
