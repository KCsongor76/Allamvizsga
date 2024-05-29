import React, { useContext, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { UserContext } from "../App";
import Row from "./Row";

import classes from "./MyProfilePage.module.css";

const MyProfilePage = () => {
  const { username } = useParams();
  const userId = useContext(UserContext);
  const [userStats, setUserStats] = useState([]);
  console.log("MyProfilePage");

  const fetchProfileStats = () => {
    const requestData = {
      userId: userId,
    };
    // Send a POST request to the Flask backend
    fetch("/get_user_stats", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => {
        console.log(response);
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
        setUserStats(data);
      })
      .catch((error) => {
        console.error("There was a problem with the fetch operation:", error);
      });
  };

  useEffect(() => {
    console.log("useeffect runs");
    fetchProfileStats();
  }, []);

  if (userStats && userStats.movies) {
    console.log(userStats.movies);
    console.log(JSON.stringify(userStats.movies));
  }

  return (
    <>
      <div className={classes.profileContainer}>
        <h1 className={classes.profileTitle}>My Profile Page - {username}</h1>
        {userStats && (
          <>
            <p className={classes.profileText}>
              Actors: {userStats.actors ? userStats.actors : "None"}
            </p>
            <p className={classes.profileText}>
              Genres: {userStats.genres ? userStats.genres : "None"}
            </p>
            <p className={classes.stats}>
              # of rated movies: {userStats.stats ? userStats.stats.count : 0}
            </p>
            <p className={classes.stats}>
              Your average rating:{" "}
              {userStats.stats ? userStats.stats.avg : "N/A"}
            </p>
          </>
        )}
      </div>
      {userStats.movies && <Row movies={userStats.movies} isProfile={true} />}
    </>
  );
};

export default MyProfilePage;
