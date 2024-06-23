import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import classes from "./MovieCard.module.css";
import { UserContext } from "../App";
import { navigateHandler } from "../functions/movieCardFunctions";

const MovieCard = ({ item, index, isProfile, quantity }) => {
  const navigate = useNavigate();
  const { username, userId } = useContext(UserContext);

  // Define the width based on the quantity
  const getWidth = (quantity) => {
    switch (quantity) {
      case 2:
        return "40%";
      case 3:
        return "30%";
      case 4:
        return "20%";
      case 5:
      case 6:
        return "15%";
      default:
        return "100%"; // Default width if no matching quantity
    }
  };

  const cardStyle = {
    width: getWidth(quantity),
  };

  return (
    <div
      key={index}
      className={classes.item}
      style={cardStyle}
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
