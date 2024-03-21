import React from "react";
import classes from './Module.module.css';

const Module = (props) => {
    // let coords = props.module['coordinates'].split(", ");
    let left = `${Math.floor(parseFloat(props.module['xCoordinate']))}%`;
    let top = `${Math.floor(parseFloat(props.module['yCoordinate']))}%`;
    
    const style = {"left": left, "top": top}

    return ( <img src={require('../../assets/module.png')} className={classes.Image} style={style} alt="Module" /> );
}

export default Module;