import React from "react";
import { deleteRatingHandler } from "../functions/movieDetailPageFunctions";

const DeleteRatingForm = ({ movie, userId, setRating }) => {
  return (
    <form
      onSubmit={(event) => deleteRatingHandler(event, movie, userId, setRating)}
    >
      <button style={{ backgroundColor: "red" }} type="submit">
        Delete rating
      </button>
    </form>
  );
};

export default DeleteRatingForm;
