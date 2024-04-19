import {useState} from "react";
import {createBrowserRouter, RouterProvider} from "react-router-dom";

import './App.css';
import MainPage from "./pages/MainPage";
import LoginPage from "./pages/LoginPage";
import RootLayout from "./pages/RootLayout";
import MovieDetailPage from "./pages/MovieDetailPage";
import ErrorPage from "./pages/ErrorPage";

function App() {
    const [isAuth, setIsAuth] = useState(false);
    const [recommendedMovies, setRecommendedMovies] = useState([]);
    const authHandler = (result) => {
        // if (!result.message) {
        //     // recommended
        //     setIsAuth(true);
        //     setRecommendedMovies(result);
        //     console.log(result);
        // }

        console.log(result);
        if (!result.message) {
            setIsAuth(true);
            result[1] = result[1].map(movie => JSON.stringify(movie));

            setRecommendedMovies(result)
        }

    }

    const router = createBrowserRouter([
        {
            path: "/",
            element: <RootLayout onAuth={state => setIsAuth(state)}/>,
            errorElement: <ErrorPage/>,
            children: [
                {index: true, element: <MainPage recommendedMovies={recommendedMovies}/>},
                {path: "/:movieId", element: <MovieDetailPage/>},
            ],
        },
    ]);

    return isAuth ? <RouterProvider router={router}/> : <LoginPage onAuth={authHandler}/>;
}

export default App;
