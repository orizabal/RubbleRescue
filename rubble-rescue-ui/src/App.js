import { useState } from 'react';
import './App.css';
import VictimInfoPopUp from './components/victimMapInfo/VictimInfoPopUp';
import DeleteVictimPopUp from './components/deleteVictim/DeleteVictimPopUp';
import SidePanel from './components/hoc/sidePanel/SidePanel';
import Map from './components/hoc/map/Map';

function App() {
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
    setVictimToDelete(null);
  }

  return (
    <div className="App">
      <SidePanel onDelete={handleSelectDelete} onSelect={handleSelectListItem} selectedVictim={selectedVictim} />
      <Map selectedVictim={selectedVictim} onCloseVictimInfo={closeVictimPopUp} />
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
