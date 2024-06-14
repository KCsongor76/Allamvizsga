import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import classes from "./MovieCard.module.css";
import { UserContext } from "../App";
import { navigateHandler } from "../functions/movieCardFunctions";

const MovieCard = ({ item, index, isProfile }) => {
  const navigate = useNavigate();
  const { username, userId } = useContext(UserContext);

  return (
    <div
      key={index}
      className={classes.item}
      onClick={() =>
        navigateHandler(index, username, userId, item, isProfile, navigate)
      }
    >
      <p>{item.title}</p>
      <img src={item.poster} alt={item.title} />
    </div>
  );
};

export default MovieCard;
