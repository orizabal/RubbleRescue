import React from "react";
import classes from './Module.module.css';

const Module = (props) => {
    let coords = props.module['coordinates'].split(", ");
    let left = `${Math.floor(parseFloat(coords[0]))}%`;
    let top = `${Math.floor(parseFloat(coords[1]))}%`;
    
    const style = {"left": left, "top": top}

    return ( <img src={require('../../assets/module.png')} className={classes.Image} style={style} /> );
}

export default Module;