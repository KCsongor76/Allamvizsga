import React, { useContext } from "react";
import classes from "./MyProfilePage.module.css";
import { UserContext } from "../App";

const ProfileDataComponent = ({ userStats }) => {
  const { username } = useContext(UserContext);

  return (
    <div className={classes.profileContainer}>
      <h1 className={classes.profileTitle}>My Profile Page - {username}</h1>
      {userStats && (
        <>
          <p className={classes.profileText}>
            Actors: {userStats.actors ? userStats.actors : "N/A"}
          </p>
          <p className={classes.profileText}>
            Genres: {userStats.genres ? userStats.genres : "N/A"}
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
