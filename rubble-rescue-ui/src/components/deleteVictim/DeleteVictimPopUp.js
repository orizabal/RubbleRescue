import {useState, React} from "react";
import classes from './DeleteVictimPopUp.module.css';

const DeleteVictimPopUp = (props) => {
    const [checked, setChecked] = useState(props.victim.truePositive);

    return (
        <div className={classes.PopUp} >
            <div className={classes.Header}>
                    <label className={classes.Label} >Remove victim {props.victim.victimId} from list?</label>
                    <button onClick={props.onClose}>X</button>
            </div>
            <div className={classes.Body}>
                <p className={classes.Coordinates} >Coordinates: {props.victim.xCoordinate}, {props.victim.yCoordinate}</p>
                <p className={classes.FoundAt} >Detected at: {props.victim.foundAt}</p>
                <div className={classes.Check}>
                    <p>True positive?</p>
                    <input type="checkbox" id="truePositive" checked={checked} onChange={e => setChecked(e.target.checked)} />
                </div>
            </div>
            <div className={classes.Buttons}>
                <button onClick={() => props.onConfirm(checked)}>Confirm</button>
                <button onClick={props.onCancel}>Cancel</button>
            </div>
        </div>
    );
}

export default DeleteVictimPopUp;
