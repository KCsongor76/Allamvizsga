// ProfileForm.js - more
export const profileSubmitHandler = (
  event,
  selectedGenres,
  selectedActors,
  userId,
  onCreateProfile,
  username,
) => {
  event.preventDefault();
  const form = event.target;

  // Prepare data to send
  const formData = new FormData(form);
  const selectedData = {
    selectedGenres,
    selectedActors,
    userId,
  };

  // Append selectedGenres and selectedActors to formData
  formData.append("selectedData", JSON.stringify(selectedData));

  fetch(form.action, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log({ ...data, username });
      if (data.message) {
        alert(data.message + "!");
      }
      onCreateProfile({ ...data, username });
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

export const handleSelectGenre = (
  genre,
  selectedGenres,
  nonSelectedGenres,
  setNonSelectedGenres,
  setSelectGenreValue,
  setSelectedGenres
) => {
  if (genre === "") return; // Prevent selecting the default option
  const updatedNonSelectedGenres = nonSelectedGenres.filter((g) => g !== genre);
  const updatedSelectedGenres = [...selectedGenres, genre];

  setNonSelectedGenres(updatedNonSelectedGenres.sort());
  setSelectedGenres(updatedSelectedGenres.sort());
  setSelectGenreValue(""); // Reset select value to default
};

export const handleDeselectGenre = (
  genre,
  selectedGenres,
  nonSelectedGenres,
  setNonSelectedGenres,
  setSelectedGenres
) => {
  const updatedSelectedGenres = selectedGenres.filter((g) => g !== genre);
  const updatedNonSelectedGenres = [...nonSelectedGenres, genre];

  setSelectedGenres(updatedSelectedGenres.sort());
  setNonSelectedGenres(updatedNonSelectedGenres.sort());
};

export const handleSelectActor = (
  actor,
  selectedActors,
  nonSelectedActors,
  setNonSelectedActors,
  setSelectedActors,
  setSelectActorValue
) => {
  if (actor === "") return; // Prevent selecting the default option
  const updatedNonSelectedActors = nonSelectedActors.filter((a) => a !== actor);
  const updatedSelectedActors = [...selectedActors, actor];

  setNonSelectedActors(updatedNonSelectedActors.sort());
  setSelectedActors(updatedSelectedActors.sort());
  setSelectActorValue(""); // Reset select value to default
};

export const handleDeselectActor = (
  actor,
  selectedActors,
  nonSelectedActors,
  setNonSelectedActors,
  setSelectedActors
) => {
  const updatedSelectedActors = selectedActors.filter((a) => a !== actor);
  const updatedNonSelectedActors = [...nonSelectedActors, actor];

  setSelectedActors(updatedSelectedActors.sort());
  setNonSelectedActors(updatedNonSelectedActors.sort());
};
