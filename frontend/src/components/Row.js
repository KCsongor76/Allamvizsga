import React, { useState, useEffect } from "react";
import classes from "./Row.module.css";
import MovieComponent from "./MovieComponent";
import { calculateItemsPerPage } from "../functions/rowFunctions";

const Row = ({ movies, isProfile }) => {
  const itemsPerPage = calculateItemsPerPage(); // Calculate items per page based on resolution
  const [currentPage, setCurrentPage] = useState(0);
  const totalPages = movies.length + 1 - itemsPerPage;
  const visibleItems = movies.slice(currentPage, currentPage + itemsPerPage);
  console.log("visibleItems: ", visibleItems);

  const handlePrevClick = () => {
    setCurrentPage((prevPage) => Math.max(0, prevPage - 1));
  };

  const handleNextClick = () => {
    setCurrentPage((prevPage) => Math.min(totalPages - 1, prevPage + 1));
  };

  useEffect(() => {
    setCurrentPage(0);
  }, [itemsPerPage, window.innerWidth]); // Reset current page when items per page change

  return (
    <div className={classes.row_container}>
      <div className={classes.navigation_buttons}>
        <button onClick={handlePrevClick} disabled={currentPage === 0}>
          {"<"}
        </button>
        <button
          onClick={handleNextClick}
          disabled={currentPage === totalPages - 1 || totalPages <= 0}
        >
          {">"}
        </button>
      </div>
      <div className={classes.item_container}>
        {movies.length > 0 ? (
          visibleItems.map((item, index) => (
            <MovieComponent key={index} item={item} index={index} isProfile={isProfile} />
          ))
        ) : (
          <p style={{ color: "red" }}>No Recommended Movies.</p>
        )}
      </div>
    </div>
  );
};

export default Row;
