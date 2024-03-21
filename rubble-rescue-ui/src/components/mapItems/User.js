import {useState, React} from "react";
import classes from './User.module.css';

const User = () => {
    const [position, setPosition] = useState(null);

    const success = (p) => {
        let lat = p.coords.latitude;
        let lng = p.coords.longitude;
        setPosition([lat, lng]);
    }

    const error = () => {
        console.log('Error getting user\'s current position.');
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, error)
    }

    let left = position ? Math.floor(position[0])  + 8: null;
    let top = position ? Math.floor(position[1]) + 22 : null;

    if (left < 0) left += 100;
    if (top < 0) top += 100;
    
    const style = position ? {"left": `${left}%`, "top": `${top}%`} : null;
    // console.log("Current position: " + position);
    return ( <img src={require('../../assets/you.png')} className={classes.Image} style={style} alt="User" /> ); // style={style}
}

export default User;