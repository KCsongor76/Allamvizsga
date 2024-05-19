import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import classes from "./MovieComponent.module.css";
import { UserContext } from "../App";
import { navigateHandler } from "../functions/movieComponentFunctions";

const MovieComponent = ({ item, index, isProfile }) => {
  const navigate = useNavigate();
  const userId = useContext(UserContext);
  console.log(item);

  return (
    <div
      key={index}
      className={classes.item}
      onClick={() => navigateHandler(index, userId, item, isProfile, navigate)}
    >
      <p>{item.title}</p>
      <img src={item.poster} alt={item.title} />
    </div>
  );
};

export default MovieComponent;
