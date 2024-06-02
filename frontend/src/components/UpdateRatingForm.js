import React from "react";
import { createUpdateFetch } from "../functions/movieDetailPageFunctions";

const UpdateRatingForm = ({ movie, userId, setRating, rating, options }) => {
  return (
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
  );
};

export default UpdateRatingForm;
