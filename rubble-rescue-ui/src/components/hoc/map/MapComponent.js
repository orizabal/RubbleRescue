import {useState, useCallback, React, useRef} from "react";
import {GoogleMap, useJsApiLoader} from '@react-google-maps/api';
import VictimInfoPopUp from "../../victimMapInfo/VictimInfoPopUp";
import Module from "../../victim/Victim";
import classes from './Map.module.css';

function MapComponent(props) {
    const [map, setMap] = useState(null);
    const {isLoaded} = useJsApiLoader({
        id: 'google-map-script',
        googleMapsApiKey: "" // TODO: Get key from envars
    });

    let containerStyle = {
        width: '80vw',
        height: '100vh'
    }

    let center = {
        lat: 43.65,
        lng: -79.38
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
                            coordinates={props.selectedVictim.coordinates}
                            foundAt={props.selectedVictim.foundAt} 
                            onClose={props.onCloseVictimInfo}
                        />
                    }
                    { props.victims.map((v) => <Module module={v} />) }
                </ GoogleMap >
            }
        </div>
    );
}

export default MapComponent;
