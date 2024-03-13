import React from "react";
import classes from './VictimInfoPopUp.module.css';

const VictimInfoPopUp = (props) => {
    return (
        <div className={classes.PopUp}>
            <div className={classes.Header}>
                <label className={classes.Label} >{props.victimId}</label>
                <button onClick={props.onClose}>X</button>
            </div>
            <div className={classes.Body}>
                <p className={classes.Coordinates} >{props.coordinates}</p>
                <p className={classes.FoundAt} >{props.foundAt}</p>
            </div>
        </div>
    );
}

export default VictimInfoPopUp;