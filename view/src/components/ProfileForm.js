import React, { useState } from "react";
import classes from "./ProfileForm.module.css";
import {
  handleDeselectActor,
  handleDeselectGenre,
  handleSelectActor,
  handleSelectGenre,
  profileSubmitHandler,
} from "../functions/profileFormFunctions";

const ProfileForm = ({ genres, actors, userId, onCreateProfile, username }) => {
  const [nonSelectedGenres, setNonSelectedGenres] = useState(genres.sort());
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [nonSelectedActors, setNonSelectedActors] = useState(actors.sort());
  const [selectedActors, setSelectedActors] = useState([]);
  const [selectGenreValue, setSelectGenreValue] = useState("");
  const [selectActorValue, setSelectActorValue] = useState("");
  const [genreSearchTerm, setGenreSearchTerm] = useState("");
  const [actorSearchTerm, setActorSearchTerm] = useState("");

  const [loading, setLoading] = useState(false);

  const filteredNonSelectedGenres = nonSelectedGenres.filter((genre) =>
    genre.toLowerCase().includes(genreSearchTerm.toLowerCase())
  );

  const filteredNonSelectedActors = nonSelectedActors
    .filter((actor) =>
      actor.toLowerCase().includes(actorSearchTerm.toLowerCase())
    )
    .slice(0, 50);

  return (
    <form
      className={classes.container}
      action="/create_profile"
      method="POST"
      onSubmit={(event) =>
        profileSubmitHandler(
          event,
          selectedGenres,
          selectedActors,
          userId,
          onCreateProfile,
          username,
          setLoading
        )
      }
    >
      <h2>Select your favourite genres and actors!</h2>
      <h3>Genres</h3>
      <label htmlFor="genre-search" className={classes.label}>
        Search genres:
      </label>

      <input
        className={classes.input}
        type="text"
        id="genre-search"
        value={genreSearchTerm}
        placeholder="Search genres..."
        onChange={(event) => setGenreSearchTerm(event.target.value)}
      />

      <select
        className={classes.select}
        id="genre-select"
        value={selectGenreValue} // Control the value of select
        onChange={(event) =>
          handleSelectGenre(
            event.target.value,
            selectedGenres,
            nonSelectedGenres,
            setNonSelectedGenres,
            setSelectGenreValue,
            setSelectedGenres
          )
        }
      >
        <option value="" disabled>
          Select a genre
        </option>
        {filteredNonSelectedGenres.map((genre) => (
          <option key={genre} value={genre}>
            {genre}
          </option>
        ))}
      </select>

      <ul className={classes.list}>
        {selectedGenres.length === 0 ? (
          <p>No selected genres.</p>
        ) : (
          selectedGenres.map((genre) => (
            <li
              className={classes.listItem}
              key={genre}
              onClick={() =>
                handleDeselectGenre(
                  genre,
                  selectedGenres,
                  nonSelectedGenres,
                  setNonSelectedGenres,
                  setSelectedGenres
                )
              }
            >
              {genre}
            </li>
          ))
        )}
      </ul>

      <h3>Actors</h3>
      <label htmlFor="actor-search" className={classes.label}>
        Search actors:
      </label>

      <input
        className={classes.input}
        type="text"
        id="actor-search"
        value={actorSearchTerm}
        placeholder="Search actors..."
        onChange={(event) => setActorSearchTerm(event.target.value)}
      />
      <select
        className={classes.select}
        id="actor-select"
        value={selectActorValue} // Control the value of select
        onChange={(event) =>
          handleSelectActor(
            event.target.value,
            selectedActors,
            nonSelectedActors,
            setNonSelectedActors,
            setSelectedActors,
            setSelectActorValue
          )
        }
      >
        <option value="" disabled>
          Select an actor
        </option>
        {filteredNonSelectedActors.map((actor) => (
          <option key={actor} value={actor}>
            {actor}
          </option>
        ))}
      </select>

      <ul className={classes.list}>
        {selectedActors.length === 0 ? (
          <p>No selected actors.</p>
        ) : (
          selectedActors.map((actor) => (
            <li
              key={actor}
              className={classes.listItem}
              onClick={() =>
                handleDeselectActor(
                  actor,
                  selectedActors,
                  nonSelectedActors,
                  setNonSelectedActors,
                  setSelectedActors
                )
              }
            >
              {actor}
            </li>
          ))
        )}
      </ul>

      <button type="submit" className={classes.button}>
        Submit
      </button>
      {loading && <div className={classes.loadingIcon} />}
    </form>
  );
};

export default ProfileForm;
