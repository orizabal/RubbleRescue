import React from "react";
import classes from './PanelHeader.module.css';

const Header = (props) => {
    return (
        <div className={classes.Header}>
            <p>{props.title}</p>
        </div>
    );
}

export default Header;
