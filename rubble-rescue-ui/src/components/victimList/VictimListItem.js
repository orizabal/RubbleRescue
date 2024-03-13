import React from 'react'; // is this needed?
import classes from './VictimListItem.module.css'

// onClick={props.onSelect
const VictimListItem = (props) => {
    let selected = props.selectedVictim ? (props.selectedVictim.victimId == props.victimId) : false
   
    return(
        <div className={selected ? classes.Selected : classes.Item} onClick={props.onSelect} >
            <div className={classes.Info} onClick={props.onSelect}>
                <label className={classes.Label} >{props.victimId}</label>
                <p className={classes.Coordinates} >{props.coordinates}</p>
                <p className={classes.FoundAt} >{props.foundAt}</p>
            </div>
            <button className={classes.Button} onClick={props.onDelete} >X</button>
        </div>
    );
}

export default VictimListItem;
