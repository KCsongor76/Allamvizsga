import { useContext, useEffect, useState } from "react";
import Row from "../components/Row";
import { UserContext } from "../App";
import { getUsernameById } from "../functions/mainPageFunctions";

const MainPage = ({ recommendedMovies }) => {
  const userId = useContext(UserContext);
  const [username, setUsername] = useState("");
  const [movieDataArray, setMovieDataArray] = useState([]);

  useEffect(() => {
    // Parse each JSON string into an object and create a new array
    const movieObjects = recommendedMovies.map((jsonString) =>
      JSON.parse(jsonString)
    );

    // Set the state with the array of parsed objects
    setMovieDataArray(movieObjects);
  }, []); // Empty dependency array to ensure useEffect runs only once

  console.log("MainPage");
  console.log(movieDataArray);

  useEffect(() => {
    getUsernameById(userId, setUsername);
  }, [userId]);

  return (
    <>
      <p>Welcome back, {username}!</p>
      <h2 style={{ color: "white" }}>Recommended Movies For You:</h2>
      <Row movies={movieDataArray} isProfile={false} />
    </>
  );
};

export default MainPage;
