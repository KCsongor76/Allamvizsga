import React, { useContext, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { UserContext } from "../App";
import Row from "./Row";

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
    <div>
      <h1>My Profile Page - {username}</h1>
      {userStats && (
        <>
          <p>Actors: {userStats.actors ? userStats.actors : "None"}</p>
          <p>Genres: {userStats.genres ? userStats.genres : "None"}</p>
          <p>
            # of rated movies: {userStats.stats ? userStats.stats.count : 0}
          </p>
          <p>
            Your average rating: {userStats.stats ? userStats.stats.avg : "N/A"}
          </p>
          {userStats.movies && <Row movies={userStats.movies} isProfile={true} />}
        </>
      )}
    </div>
  );
};

export default MyProfilePage;
