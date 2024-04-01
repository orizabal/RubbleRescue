import React from "react";
import classes from './Victim.module.css';

const Victim = (props) => {
    // let coords = props.victim['coordinates'].split(", ");
    let left = `${Math.floor(parseFloat(props.victim.xCoordinate)) + 51.1}%`;
    let top = `${Math.floor(parseFloat(props.victim.yCoordinate)) + 48.5}%`;
    
    const style = {"left": left, "top": top}

    return ( <img src={require('../../assets/victim.png')} className={classes.Image} style={style} alt="Victim" /> );
}

export default Victim;
