import { createContext, useState } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import "./App.css";
import MainPage from "./pages/MainPage";
import RootLayout from "./pages/RootLayout";
import MovieDetailPage from "./pages/MovieDetailPage";
import ErrorPage from "./pages/ErrorPage";
import AuthPage from "./pages/AuthPage";
import MyProfilePage from "./components/MyProfilePage";
import { authHandler } from "./functions/appFunctions";

export const UserContext = createContext();

function App() {
  const [isAuth, setIsAuth] = useState(false);
  const [recommendedMovies, setRecommendedMovies] = useState([]);
  const [userId, setUserId] = useState(-1);
  //console.log("recMovies: ", recommendedMovies);
  //console.log("recMovies: ", JSON.stringify(recommendedMovies));

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
        {
          path: "/users/:username",
          element: <MyProfilePage />,
        },
      ],
    },
  ]);

  return isAuth ? (
    <UserContext.Provider value={userId}>
      <RouterProvider router={router} />
    </UserContext.Provider>
  ) : (
    <AuthPage
      onAuth={(data) =>
        authHandler(data, setUserId, setIsAuth, setRecommendedMovies)
      }
      onSignUp={(data) =>
        authHandler(data, setUserId, setIsAuth, setRecommendedMovies)
      }
      isLogin={true}
    />
  );
}

export default App;
