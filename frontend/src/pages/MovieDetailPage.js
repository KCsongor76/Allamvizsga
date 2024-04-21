import React from 'react';
import {useLocation, useNavigate} from 'react-router-dom';
import classes from './MovieDetailPage.module.css';

const DetailedMoviePage = () => {
    const location = useLocation();
    const movie = location.state.movie;
    const navigate = useNavigate();

    const navigateHandler = () => {
        navigate("/")
    }

    console.log(movie);

    return (
        <>
            <div className={classes.movieContainer}>
                <div className={classes.movieDetails}>
                    <h1 className={classes.title}>{movie.title}</h1>
                    <p className={classes.description}>Plot: {movie.plot}</p>
                    <p className={classes.info}>Director: {movie.director}</p>
                    <p className={`${classes.info} ${classes.movieActors}`}>Actors: {movie.actors}</p>
                    <p className={classes.info}>Released: {movie.year}</p>
                </div>
                <img src={movie.poster} alt={movie.Title} className={classes.moviePoster}/>
            </div>
            <div className={classes.buttonContainer}>
                <button className={classes.button} onClick={navigateHandler}>Go Back</button>
            </div>
        </>
    );


};

export default DetailedMoviePage;
