import React from "react";
import classes from './Victim.module.css';

const Victim = (props) => {
    // let coords = props.victim['coordinates'].split(", ");
    console.log(props.victim.xCoordinate);
    console.log(props.victim.yCoordinate);
    let left = `${Math.floor(parseFloat(props.victim.xCoordinate)) + 51.2}%`;
    let top = `${Math.floor(parseFloat(props.victim.yCoordinate)) + 50.5}%`;
    
    const style = {"left": left, "top": top}

    return ( <img src={require('../../assets/victim.png')} className={classes.Image} style={style} alt="Victim" /> );
}

export default Victim;
