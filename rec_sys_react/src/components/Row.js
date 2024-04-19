import React, {useState, useEffect} from 'react';
import classes from "./Row.module.css";
import MovieComponent from "./MovieComponent";

const Row = ({movies}) => {
    const itemsPerPage = calculateItemsPerPage(); // Calculate items per page based on resolution
    const [currentPage, setCurrentPage] = useState(0);

    const totalPages = movies.length + 1 - itemsPerPage;
    console.log("totalPages:", totalPages)

    useEffect(() => {
        setCurrentPage(0);
    }, [itemsPerPage, window.innerWidth]); // Reset current page when items per page change

    const handlePrevClick = () => {
        setCurrentPage((prevPage) => Math.max(0, prevPage - 1));
    };

    const handleNextClick = () => {
        setCurrentPage((prevPage) => Math.min(totalPages - 1, prevPage + 1));
    };

    const visibleItems = movies.slice(
        currentPage,
        currentPage + itemsPerPage
    );

    return (
        <div className={classes.row_container}>
            <div className={classes.navigation_buttons}>
                <button onClick={handlePrevClick} disabled={currentPage === 0}>
                    {'<'}
                </button>
                <button onClick={handleNextClick} disabled={currentPage === totalPages - 1 || totalPages <= 0}>
                    {'>'}
                </button>
            </div>
            <div className={classes.item_container}>
                {movies.length > 0 ? visibleItems.map((item, index) => (
                    <MovieComponent key={index} item={item} index={index}/>
                )) : <p style={{color: "red"}}>No Recommended Movies.</p>}
            </div>
        </div>
    );
};

// Function to calculate items per page based on resolution
const calculateItemsPerPage = () => {
    // You can use window.innerWidth or any other logic to determine the resolution
    const resolution = window.innerWidth;

    // Adjust the logic based on your specific requirements
    if (resolution < 600) {
        return 2;
    } else if (resolution < 900) {
        return 4;
    } else {
        return 6;
    }
};

export default Row;
