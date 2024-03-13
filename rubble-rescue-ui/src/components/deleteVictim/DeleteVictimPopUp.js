import React from "react";
import classes from './DeleteVictimPopUp.module.css';

const DeleteVictimPopUp = (props) => {
    return (
        <div className={classes.PopUp}>
            <div className={classes.Header}>
                    <label className={classes.Label} >{props.victimId}</label>
                    <button onClick={props.onClose}>X</button>
            </div>
            <div className={classes.Body}>
                <p className={classes.Coordinates} >{props.coordinates}</p>
                <p className={classes.FoundAt} >{props.foundAt}</p>
                <p>True Positive?</p>
                <input type="checkbox" id="truePositive" value={false} />
            </div>
            <div className={classes.Buttons}>
                <button onClick={props.onConfirm}>Confirm</button>
                <button onClick={props.onCancel}>Cancel</button>
            </div>
        </div>
    );
}

export default DeleteVictimPopUp;
