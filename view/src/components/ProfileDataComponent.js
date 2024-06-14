import React, { useContext } from "react";
import classes from "./MyProfilePage.module.css";
import { UserContext } from "../App";

const ProfileDataComponent = ({ userStats }) => {
  const { username } = useContext(UserContext);

  // Function to convert '|' separated string into ' ' separated string
  const formatGenresActors = (str) => {
    if (!str) return "N/A";
    return str.split('|').join(', ');
  };

  return (
    <div className={classes.profileContainer}>
      <h1 className={classes.profileTitle}>My Profile Page - {username}</h1>
      {userStats && (
        <>
          <p className={classes.profileText}>
            Actors: {formatGenresActors(userStats.actors)}
          </p>
          <p className={classes.profileText}>
            Genres: {formatGenresActors(userStats.genres)}
          </p>
          <p className={classes.stats}>
            # of rated movies: {userStats.stats ? userStats.stats.count : 0}
          </p>
          <p className={classes.stats}>
            Your average rating: {userStats.stats ? Number(userStats.stats.avg).toFixed(2) : "N/A"}
          </p>
        </>
      )}
    </div>
  );
};

export default ProfileDataComponent;
