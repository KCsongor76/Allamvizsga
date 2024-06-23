
export const authHandler = (
  data,
  setUserId,
  setIsAuth,
  setRecommendedMovies,
  setUsername
) => {
  if (data.movies) {
    setUserId(data.user_id);
    setUsername(data.username);
    setIsAuth(true);
    const movies = data.movies.map((movie) => JSON.stringify(movie));
    setRecommendedMovies(movies);
    console.log(data);
  }
};

export const fetchAllMovies = (setAllMovies) => {
  fetch("/get_all_movies", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      setAllMovies(data);
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
};

export const profileLoader = async (userId) => {
  const response = await fetch("/get_user_stats", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ userId }),
  });

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  const data = await response.json();
  console.log(data);
  return data;
};
