import React from "react";
import VictimInfoPopUp from "../../victimMapInfo/VictimInfoPopUp";
import classes from './Map.module.css';

const Map = (props) => {
    return (
        <div>
            {props.selectedVictim &&
                <VictimInfoPopUp
                    victimId={props.selectedVictim.victimId}
                    coordinates={props.selectedVictim.coordinates}
                    foundAt={props.selectedVictim.foundAt} 
                    onClose={props.onCloseVictimInfo}
                />
            }
        </div>
    );
}

export default Map;
