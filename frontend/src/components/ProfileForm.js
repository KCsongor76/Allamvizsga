import { useState } from "react";
import {
  profileSubmitHandler,
  removeActor,
  removeGenre,
} from "../functions/profileFormFunctions";

import classes from "./ProfileForm.module.css";

const ProfileForm = ({ genres, actors, userId, onCreateProfile }) => {
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [selectedActors, setSelectedActors] = useState([]);
  const [searchGenres, setSearchGenres] = useState("");
  const [searchActors, setSearchActors] = useState("");

  return (
    <form
      className={classes.formContainer}
      action="/create_profile"
      method="POST"
      onSubmit={(event) =>
        profileSubmitHandler(
          event,
          selectedGenres,
          selectedActors,
          userId,
          onCreateProfile
        )
      }
    >
      <input
        className={classes.inputText}
        type="text"
        placeholder="Search genres..."
        value={searchGenres}
        onChange={(event) => setSearchGenres(event.target.value)}
      ></input>

      <select
        className={classes.inputText}
        onClick={(event) =>
          setSelectedGenres((prev) => {
            const newValue = event.target.value;
            console.log(newValue);
            // Check if newValue already exists in selectedGenres array
            if (!prev.includes(newValue)) {
              // If it doesn't exist, add it to the array
              return [...prev, newValue];
            } else {
              // If it exists, return the array unchanged
              return prev;
            }
          })
        }
      >
        <option disabled>Select genre</option>
        {genres
          .filter((genre) =>
            genre.toLowerCase().includes(searchGenres.toLowerCase())
          ) // Filter genres based on the search input
          .map((genre, index) => (
            <option key={index} value={genre}>
              {genre}
            </option> // added value attribute
          ))}
      </select>

      {selectedGenres.length === 0 ? (
        <p>No selected genres.</p>
      ) : (
        <ul className={classes.ul}>
          {selectedGenres.map((genre, index) => (
            <li
              className={classes.li}
              key={index}
              onClick={() => removeGenre(index, setSelectedGenres)}
            >
              {genre}
            </li>
          ))}
        </ul>
      )}

      <input
        className={classes.inputText}
        type="text"
        placeholder="Search actors..."
        value={searchActors}
        onChange={(event) => setSearchActors(event.target.value)}
      ></input>

      <select
        className={classes.select}
        onChange={(event) =>
          setSelectedActors((prev) => {
            const newValue = event.target.value;
            if (!prev.includes(newValue)) {
              return [...prev, newValue];
            } else {
              return prev;
            }
          })
        }
      >
        <option disabled>Select actor</option>
        {actors
          .filter((actor) =>
            actor.toLowerCase().includes(searchActors.toLowerCase())
          )
          .slice(0, Math.min(50, actors.length))
          .map((actor, index) => (
            <option key={index} value={actor}>
              {actor}
            </option>
          ))}
      </select>

      {selectedActors.length === 0 ? (
        <p>No selected genres.</p>
      ) : (
        <ul className={classes.ul}>
          {selectedActors.map((actor, index) => (
            <li
              className={classes.li}
              key={index}
              onClick={() => removeActor(index, setSelectedActors)}
            >
              {actor}
            </li>
          ))}
        </ul>
      )}

      <button className={classes.button} type="submit">
        Create profile!
      </button>
    </form>
  );
};

export default ProfileForm;
