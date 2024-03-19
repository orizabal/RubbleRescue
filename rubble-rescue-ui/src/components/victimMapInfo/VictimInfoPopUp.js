import React from "react";
import classes from './VictimInfoPopUp.module.css';

const VictimInfoPopUp = (props) => {
    let coords = props.coordinates.split(", ");
    let left = `${Math.floor(parseFloat(coords[0])) + 1}%`;
    let topVal = Math.floor(parseFloat(coords[1])) - 10;
    let top = `${topVal < 0 ? (topVal + 14) : topVal}%`;
    
    const style = {"left": left, "top": top}

    return (
        <div className={classes.PopUp} style={style}>
            <div className={classes.Header}>
                <label className={classes.Label} >Victim {props.victimId} Info</label>
                <button onClick={props.onClose}>X</button>
            </div>
            <div className={classes.Body}>
                <p className={classes.Coordinates} >Coordinates: {props.coordinates}</p>
                <p className={classes.FoundAt} >Detected at: {props.foundAt}</p>
            </div>
        </div>
    );
}

export default VictimInfoPopUp;