// MovieDetailPage.js
export const createUpdateFetch = (
  event,
  apiRoute,
  method,
  movie,
  userId,
  setRating
) => {
  event.preventDefault();
  const formData = new FormData(event.target);
  const newRating = formData.get("rating");

  fetch(apiRoute, {
    method: method,
    body: new URLSearchParams({
      movieId: movie.id,
      userId: userId,
      rating: newRating,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data.message);
      setRating(newRating);
    })
    .catch((error) => console.error("Error:", error));
};

export const deleteRatingHandler = (event, movie, userId, setRating) => {
  event.preventDefault();
  fetch("/delete_rating", {
    method: "DELETE",
    body: new URLSearchParams({
      movieId: movie.id,
      userId: userId,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      setRating(undefined);
    })
    .catch((error) => console.error("Error:", error));
};
