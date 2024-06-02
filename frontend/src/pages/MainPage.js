import { useContext, useEffect, useState } from "react";
import Row from "../components/Row";
import { UserContext } from "../App";
import LabelInput from "../components/FormElements/LabelInput";
import classes from './MainPage.module.css';

const MainPage = ({ recommendedMovies }) => {
  const { username, allMovies } = useContext(UserContext);
  const [movieDataArray, setMovieDataArray] = useState([]);
  const [searchTitle, setSearchTitle] = useState("");

  useEffect(() => {
    // Parse each JSON string into an object and create a new array
    const movieObjects = recommendedMovies.map((jsonString) =>
      JSON.parse(jsonString)
    );
    setMovieDataArray(movieObjects);
  }, [recommendedMovies]);

  return (
    <>
      <p style={{ color: "white" }}>Welcome back, {username}!</p>
      <h2 style={{ color: "white" }}>Recommended Movies For You:</h2>
      <Row movies={movieDataArray} isProfile={false} />
      {allMovies.allMovies && (
        <>
          <h2 style={{ color: "white" }}>Search movies:</h2>
          <div className={classes.labelContainer}>
            <LabelInput
              type="text"
              id="search_movies"
              name="search_movies"
              value={searchTitle}
              setter={setSearchTitle}
              placeholder="Search title..."
            />
          </div>
          <Row
            movies={allMovies.allMovies.filter((movie) =>
              movie.title.toLowerCase().includes(searchTitle.toLowerCase())
            )}
            isProfile={false}
          />
        </>
      )}
    </>
  );
};

export default MainPage;
