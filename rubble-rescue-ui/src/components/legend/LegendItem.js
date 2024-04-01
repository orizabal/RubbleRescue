import React from "react";
import classes from './LegendItem.module.css';

const LegendItem = (props) => {
    return (
        <div className={classes.LegendItem}>
            <img src={require(`../../assets/${props.img}`)} className={classes.Image} />
            <p>{props.itemName}</p>
        </div>
    );
}

export default LegendItem;
