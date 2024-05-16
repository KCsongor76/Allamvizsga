import { useState } from "react";

const ProfileForm = ({ genres, actors, onCreateProfile }) => {
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [selectedActors, setSelectedActors] = useState([]);
  const [searchGenres, setSearchGenres] = useState("");
  const [searchActors, setSearchActors] = useState("");

  const submitHandler = (event) => {
    event.preventDefault();
    const form = event.target;

    // Prepare data to send
    const formData = new FormData(form);
    const selectedData = {
      selectedGenres,
      selectedActors,
    };

    // Append selectedGenres and selectedActors to formData
    formData.append("selectedData", JSON.stringify(selectedData));

    fetch(form.action, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        onCreateProfile(data)
      })
      .catch((error) => console.error("Error:", error));
  };

  const removeGenre = (index) => {
    setSelectedGenres((prevGenres) => {
      const newGenres = [...prevGenres];
      newGenres.splice(index, 1); // Remove the genre at the given index
      return newGenres;
    });
  };

  const removeActor = (index) => {
    setSelectedActors((prevActors) => {
      const newActors = [...prevActors];
      newActors.splice(index, 1); // Remove the genre at the given index
      return newActors;
    });
  };

  return (
    <form action="/create_profile" method="POST" onSubmit={submitHandler}>
      <input
        type="text"
        placeholder="Search genres..."
        value={searchGenres}
        onChange={(event) => setSearchGenres(event.target.value)}
      ></input>

      <select
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
        <ul>
          {selectedGenres.map((genre, index) => (
            <li key={index} onClick={() => removeGenre(index)}>
              {genre}
            </li>
          ))}
        </ul>
      )}

      <input
        type="text"
        placeholder="Search actors..."
        value={searchActors}
        onChange={(event) => setSearchActors(event.target.value)}
      ></input>

      <select
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
        <ul>
          {selectedActors.map((actor, index) => (
            <li key={index} onClick={() => removeActor(index)}>
              {actor}
            </li>
          ))}
        </ul>
      )}

      <button type="submit">Create profile!</button>
    </form>
  );
};

export default ProfileForm;
