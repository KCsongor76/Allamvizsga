import { useLocation, useNavigate } from "react-router-dom";
import classes from "./MovieDetailPage.module.css";
import { useEffect, useState } from "react";
import {
  createUpdateFetch,
  deleteRatingHandler,
} from "../functions/movieDetailPageFunctions";
import { getUsernameById } from "../functions/mainPageFunctions";

const DetailedMoviePage = () => {
  const location = useLocation();
  const movie = location.state.movie;
  const userId = location.state.userId;
  const isProfile = location.state.isProfile;

  const [rating, setRating] = useState(location.state.rating);
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  const navigateHandler = () => {
    if (isProfile) {
      navigate(`/users/${username}`);
    } else {
      navigate("/");
    }
  };

  // Define the options values
  const values = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5];
  // Create an array to hold the JSX options
  const options = [];
  // Loop through the values array and create options
  for (let i = 0; i < values.length; i++) {
    options.push(
      <option key={i} value={values[i]}>
        {values[i]}
      </option>
    );
  }

  useEffect(() => {
    getUsernameById(userId, setUsername);
  }, [userId]);

  return (
    <>
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
      <button className={classes.button} onClick={navigateHandler}>
        Go Back
      </button>

      {!isNaN(rating) && (
        <>
          <form
            onSubmit={(event) =>
              createUpdateFetch(
                event,
                "/update_rating",
                "PUT",
                movie,
                userId,
                setRating
              )
            }
          >
            <p>Your Rating: {rating}</p>
            <p>Change rating: </p>
            <select name="rating">{options}</select>
            <button type="submit">Update rating</button>
          </form>

          <form
            onSubmit={(event) =>
              deleteRatingHandler(event, movie, userId, setRating)
            }
          >
            <button type="submit">Delete rating</button>
          </form>
        </>
      )}

      {isNaN(rating) && (
        <form
          onSubmit={(event) =>
            createUpdateFetch(
              event,
              "/add_rating",
              "POST",
              movie,
              userId,
              setRating
            )
          }
        >
          <p>Add rating: </p>
          <select name="rating">{options}</select>
          <button type="submit">Add rating</button>
        </form>
      )}
    </>
  );
};

export default DetailedMoviePage;
