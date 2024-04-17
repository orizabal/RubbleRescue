import {useState, useCallback, React} from "react";
import {GoogleMap, useJsApiLoader} from '@react-google-maps/api';
import VictimInfoPopUp from "../../victimMapInfo/VictimInfoPopUp";
import Victim from "../../mapItems/Victim";
import classes from './Map.module.css';
import Module from "../../mapItems/Module";
import User from "../../mapItems/User";

function MapComponent(props) {
    const [map, setMap] = useState(null);
    const {isLoaded} = useJsApiLoader({
        id: 'google-map-script',
        googleMapsApiKey: "AIzaSyAnkMo9wS_8NNMb5H9-cParvjYdmriy3J0" // TODO: Get key from envars
    });

    let containerStyle = {
        width: '80vw',
        height: '100vh'
    }

    let center = {
        lat: 43.47309465699636,
        lng: -80.53950340308066
    }

    const onLoad = useCallback(function callback(map) {
        const bounds = new window.google.maps.LatLngBounds(center);
        map.fitBounds(bounds);
    }, []);

    const onUnmount = useCallback(function callback(map) {
        setMap(map);
    }, []);

    return (
        <div>
            {isLoaded &&
                <GoogleMap
                    className={classes.Map}
                    mapContainerStyle={containerStyle}
                    center={center}
                    zoom={10}
                    onLoad={onLoad}
                    onUnmount={onUnmount}
                >
                    {props.selectedVictim &&
                        <VictimInfoPopUp
                            victimId={props.selectedVictim.victimId}
                            xCoordinate={props.selectedVictim.xCoordinate}
                            yCoordinate={props.selectedVictim.yCoordinate}
                            foundAt={props.selectedVictim.foundAt} 
                            onClose={props.onCloseVictimInfo}
                        />
                    }
                    { props.victims.map((v) => <Victim victim={v} key={v['victimId']} />) }
                    { props.modules.map((m) => <Module module={m} key={m['id']} />) }
                    {/* { position && <User position={[position[0], position[1]]} /> } */}
                    <User />
                </ GoogleMap >
            }
        </div>
    );
}

export default MapComponent;
