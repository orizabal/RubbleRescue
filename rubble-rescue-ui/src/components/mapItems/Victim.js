import React from "react";
import classes from './Victim.module.css';

const Victim = (props) => {
    // let coords = props.victim['coordinates'].split(", ");
    let left = `${Math.floor(parseFloat(props.xCoordinate))}%`;
    let top = `${Math.floor(parseFloat(props.yCoordinate))}%`;
    
    const style = {"left": left, "top": top}

    return ( <img src={require('../../assets/victim.png')} className={classes.Image} style={style} alt="Victim" /> );
}

export default Victim;
