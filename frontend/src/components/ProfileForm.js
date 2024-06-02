import { useState } from "react";
import {
  profileSubmitHandler,
  removeActor,
  removeGenre,
  //selectActors,
  //selectGenres,
} from "../functions/profileFormFunctions";

import classes from "./ProfileForm.module.css";
import LabelInput from "./FormElements/LabelInput";

const ProfileForm = ({ genres, actors, userId, onCreateProfile, username }) => {
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [selectedActors, setSelectedActors] = useState([]);
  const [searchGenres, setSearchGenres] = useState("");
  const [searchActors, setSearchActors] = useState("");

  const filteredGenres = genres
    .filter((genre) => genre.toLowerCase().includes(searchGenres.toLowerCase()))
    .sort((a, b) => a.localeCompare(b));

  const genreOptions = filteredGenres.map((genre, index) => (
    <option
      key={index}
      value={genre}
      onClick={() => {
        console.log(genre);
        selectGenresHandler(genre);
      }}
    >
      {genre}
    </option> // added value attribute
  ));

  const selectedGenresList = selectedGenres.map((genre, index) => (
    <li
      className={classes.li}
      key={index}
      onClick={() => removeGenre(index, setSelectedGenres)}
    >
      {genre}
    </li>
  ));

  const filteredActors = actors
    .filter((actor) => actor.toLowerCase().includes(searchActors.toLowerCase()))
    .sort((a, b) => a.localeCompare(b));

  const slicedActors = filteredActors.slice(0, Math.min(50, actors.length));

  const actorsOptions = slicedActors.map((actor, index) => (
    <option
      key={index}
      value={actor}
      onClick={() => {
        console.log(actor);
        selectActorsHandler(actor);
      }}
    >
      {actor}
    </option>
  ));

  const selectedActorsList = selectedActors.map((actor, index) => (
    <li
      className={classes.li}
      key={index}
      onClick={() => removeActor(index, setSelectedActors)}
    >
      {actor}
    </li>
  ));

  const selectGenresHandler = (genre) => {
    console.log(genre);
    setSelectedGenres((prev) => {
      return prev.includes(genre) ? prev : [...prev, genre];
    });
  };

  const selectActorsHandler = (actor) => {
    console.log("selectActorsHandler");
    console.log(actor);
    setSelectedActors((prev) => {
      return prev.includes(actor) ? prev : [...prev, actor];
    });
  };

  /*const selectGenres = (event, setSelectedGenres) => {
    const newValue = event.target.value;
    setSelectedGenres((prev) => {
      return prev.includes(newValue) ? prev : [...prev, newValue];
    });
  };

  const selectActors = (event, setSelectedActors) => {
    const newValue = event.target.value;
    setSelectedActors((prev) => {
      return prev.includes(newValue) ? prev : [...prev, newValue];
    });
  };*/

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
          onCreateProfile,
          username
        )
      }
    >
      <LabelInput
        labelText=""
        type="text"
        id="search_genres"
        name="search_genres"
        value={searchGenres}
        placeholder="Search genres..."
        setter={setSearchGenres}
      />

      <select
        className={classes.inputText}
        onChange={(event) => selectGenresHandler(event.target.value)}
      >
        <option disabled selected>
          Select genre
        </option>
        {genreOptions}
      </select>

      {selectedGenres.length === 0 ? (
        <p>No selected genres.</p>
      ) : (
        <ul className={classes.ul}>{selectedGenresList}</ul>
      )}

      <LabelInput
        labelText=""
        type="text"
        id="search_actors"
        name="search_actors"
        value={searchActors}
        placeholder="Search actors..."
        setter={setSearchActors}
      />

      <select
        className={classes.select}
        onChange={(event) => selectActorsHandler(event.target.value)}
      >
        <option disabled selected>
          Select actor
        </option>
        {actorsOptions}
      </select>

      {selectedActors.length === 0 ? (
        <p>No selected actors.</p>
      ) : (
        <ul className={classes.ul}>{selectedActorsList}</ul>
      )}

      <button className={classes.button} type="submit">
        Create profile!
      </button>
    </form>
  );
};

export default ProfileForm;
