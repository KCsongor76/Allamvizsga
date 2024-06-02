import { useLocation, useNavigate } from "react-router-dom";
import classes from "./MovieDetailPage.module.css";
import { useContext, useState } from "react";
import {
  navigateHandler,
  renderAddRatingForm,
  renderUpdateDeleteForm,
} from "../functions/movieDetailPageFunctions";
import { UserContext } from "../App";
import MovieDataComponent from "../components/MovieDataComponent";

const MovieDetailPage = () => {
  const location = useLocation();
  const movie = location.state.movie;
  const { username, userId } = useContext(UserContext);
  const isProfile = location.state.isProfile;

  const [rating, setRating] = useState(location.state.rating);
  const navigate = useNavigate();

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

  return (
    <div className={classes.container}>
      <MovieDataComponent movie={movie} />

      {!isNaN(rating) &&
        renderUpdateDeleteForm(movie, userId, setRating, rating, options)}

      {isNaN(rating) && renderAddRatingForm(movie, userId, options, setRating)}
      <div className={classes.buttonContainer}>
        <button
          className={classes.button}
          onClick={() => navigateHandler(isProfile, username, navigate)}
        >
          Go Back
        </button>
      </div>
    </div>
  );
};

export default MovieDetailPage;
