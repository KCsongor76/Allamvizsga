import React from "react";
import classes from "./MovieDataComponent.module.css";

const MovieDataComponent = ({ movie }) => {
  return (
    <div className={classes.movieContainer}>
      <div className={classes.movieDetails}>
        <h1 className={classes.title}>{movie.title}</h1>
        <p className={classes.description}>Plot: {movie.plot}</p>
        <p className={classes.info}>Director: {movie.director}</p>
        <p className={`${classes.info} ${classes.movieActors}`}>
          Actors: {movie.actors}
        </p>
        <p className={classes.info}>Released: {movie.year}</p>
      </div>
      <img
        src={movie.poster}
        alt={movie.title}
        className={classes.moviePoster}
      />
    </div>
  );
};

export default MovieDataComponent;
