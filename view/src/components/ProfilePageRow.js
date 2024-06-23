import React, { useState, useEffect } from "react";
import classes from "./Row.module.css";
import MovieCard from "./MovieCard";
import {
  calculateItemsPerPage,
  handleNextClick,
  handlePrevClick,
} from "../functions/rowFunctions";

const ProfilePageRow = ({ movies, isProfile }) => {
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const itemsPerPage = calculateItemsPerPage(windowWidth); // Calculate items per page based on resolution
  const [currentPage, setCurrentPage] = useState(0);
  const totalPages = movies.length + 1 - itemsPerPage;
  const visibleItems = movies.slice(currentPage, currentPage + itemsPerPage);

  useEffect(() => {
    setCurrentPage(0);
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };

    // Add event listener for window resize
    window.addEventListener("resize", handleResize);

    // Cleanup function to remove the event listener
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [itemsPerPage]); // Reset current page when items per page change

  return (
    <div className={classes.row_container}>
      <div className={classes.navigation_buttons}>
        <button
          onClick={() => handlePrevClick(setCurrentPage)}
          disabled={currentPage === 0}
          style={{ cursor: !(currentPage === 0) ? "pointer" : "default" }}
        >
          {"<"}
        </button>
        <button
          onClick={() => handleNextClick(totalPages, setCurrentPage)}
          disabled={currentPage === totalPages - 1 || totalPages <= 0}
          style={{
            cursor: !(currentPage === totalPages - 1 || totalPages <= 0)
              ? "pointer"
              : "default",
          }}
        >
          {">"}
        </button>
      </div>
      <div className={classes.item_container}>
        {movies.length > 0 ? (
          visibleItems.map((item, index) => (
            <MovieCard
              key={index}
              item={item}
              index={index}
              isProfile={isProfile}
              quantity={visibleItems.length}
            />
          ))
        ) : (
          <p style={{ color: "red" }}>No Recommended Movies.</p>
        )}
      </div>
    </div>
  );
};

export default ProfilePageRow;
