import React from "react";
import {useNavigate} from "react-router-dom";
import classes from './MovieComponent.module.css';

const MovieComponent = ({item, index}) => {
    const navigate = useNavigate();
    const navigateHandler = (index) => {
        navigate(`${index}`, {state: {movie: JSON.parse(item)}});
    }

    return (
        <div
            key={index}
            className={classes.item}
            onClick={() => navigateHandler(index)}
        >
            <p>{JSON.parse(item).title}</p>
            <img src={JSON.parse(item).poster} alt={JSON.parse(item).title}/>
        </div>
    );
}

export default MovieComponent;