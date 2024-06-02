// ProfileForm.js - more
export const profileSubmitHandler = (
  event,
  selectedGenres,
  selectedActors,
  userId,
  onCreateProfile,
  username
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
    .catch((error) => console.error("Error:", error));
};

export const removeGenre = (index, setSelectedGenres) => {
  setSelectedGenres((prevGenres) => {
    const newGenres = [...prevGenres];
    newGenres.splice(index, 1); // Remove the genre at the given index
    return newGenres;
  });
};

export const removeActor = (index, setSelectedActors) => {
  setSelectedActors((prevActors) => {
    const newActors = [...prevActors];
    newActors.splice(index, 1); // Remove the actor at the given index
    return newActors;
  });
};

export const selectGenres = (event, setSelectedGenres) => {
  const newValue = event.target.value;
  setSelectedGenres((prev) => {
    return prev.includes(newValue) ? prev : [...prev, newValue];
  });
};

export const selectActors = (event, setSelectedActors) => {
  const newValue = event.target.value;
  setSelectedActors((prev) => {
    return prev.includes(newValue) ? prev : [...prev, newValue];
  });
};
