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
                    <h1 className={classes.title}>{movie.Title}</h1>
                    <p className={classes.description}>Plot: {movie.Plot}</p>
                    <p className={classes.info}>Director: {movie.Director}</p>
                    <p className={`${classes.info} ${classes.movieActors}`}>Actors: {movie.Actors}</p>
                    <p className={classes.info}>Released: {movie.Released}</p>
                    <p className={classes.info}>Language: {movie.Language}</p>
                </div>
                <img src={movie.Poster} alt={movie.Title} className={classes.moviePoster}/>
            </div>
            <div className={classes.buttonContainer}>
                <button className={classes.button} onClick={navigateHandler}>Go Back</button>
            </div>
        </>
    );


};

export default DetailedMoviePage;
