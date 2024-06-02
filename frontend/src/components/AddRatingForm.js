import React from "react";
import { createUpdateFetch } from "../functions/movieDetailPageFunctions";

const AddRatingForm = ({ movie, userId, options, setRating }) => {
  return (
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
  );
};

export default AddRatingForm;
