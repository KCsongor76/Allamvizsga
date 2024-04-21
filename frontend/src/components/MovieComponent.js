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
            <p>{JSON.parse(item).Title}</p>
            <img src={JSON.parse(item).Poster} alt={JSON.parse(item).Title}/>
        </div>
    );
}

export default MovieComponent;