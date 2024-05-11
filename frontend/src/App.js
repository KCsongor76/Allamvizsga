import { useState } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import "./App.css";
import MainPage from "./pages/MainPage";
import RootLayout from "./pages/RootLayout";
import MovieDetailPage from "./pages/MovieDetailPage";
import ErrorPage from "./pages/ErrorPage";
import AuthPage from "./pages/AuthPage";

function App() {
  const [isAuth, setIsAuth] = useState(false);
  const [recommendedMovies, setRecommendedMovies] = useState([]);
  const authHandler = (result) => {
    console.log(result);
    if (!result.message) {
      setIsAuth(true);
      result = result.map((movie) => JSON.stringify(movie));

      setRecommendedMovies(result);
    }
  };

  const router = createBrowserRouter([
    {
      path: "/",
      element: <RootLayout onAuth={(state) => setIsAuth(state)} />,
      errorElement: <ErrorPage />,
      children: [
        {
          index: true,
          element: <MainPage recommendedMovies={recommendedMovies} />,
        },
        { path: "/:movieId", element: <MovieDetailPage /> },
      ],
    },
  ]);

  return isAuth ? (
    <RouterProvider router={router} />
  ) : (
    <AuthPage onAuth={authHandler} isLogin={true} />
  );
}

export default App;
