import {useState} from "react";
import Row from "../components/Row";

const MainPage = ({recommendedMovies}) => {

    return (
        <>
            <h2 style={{color: "white"}}>Recommended Movies For You:</h2>
            <Row movies={recommendedMovies}/>
            {/*<h2 style={{color: "white"}}>Generally good movies:</h2>
            <Row movies={recommendedMovies[1]}/>*/}
        </>
    );
}

export default MainPage;