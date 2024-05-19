export const authHandler = (
  data,
  setUserId,
  setIsAuth,
  setRecommendedMovies
) => {
  if (data.movies) {
    setUserId(data.user_id);
    setIsAuth(true);
    const movies = data.movies.map((movie) => JSON.stringify(movie));
    setRecommendedMovies(movies);
    console.log("App login through")
  }
};
