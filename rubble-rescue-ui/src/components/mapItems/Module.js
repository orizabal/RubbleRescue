import React from "react";
import classes from './Module.module.css';

const Module = (props) => {
    // let coords = props.module['coordinates'].split(", ");
    let left = `${Math.floor(parseFloat(props.module['xCoordinate'])) + 40}%`;
    let top = `${Math.floor(parseFloat(props.module['yCoordinate'])) - 10}%`;
    
    const style = {"left": left, "top": top}

    return ( <img src={require('../../assets/module.png')} className={classes.Image} style={style} alt="Module" /> );
}

export default Module;