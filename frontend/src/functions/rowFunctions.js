//Row.js
// Function to calculate items per page based on resolution
export const calculateItemsPerPage = (windowWidth) => {
  // You can use window.innerWidth or any other logic to determine the resolution
  const resolution = windowWidth;

  // Adjust the logic based on your specific requirements
  if (resolution < 600) {
    return 2;
  } else if (resolution < 900) {
    return 4;
  } else {
    return 6;
  }
};

export const handlePrevClick = (setCurrentPage) => {
  setCurrentPage((prevPage) => Math.max(0, prevPage - 1));
};

export const handleNextClick = (totalPages, setCurrentPage) => {
  setCurrentPage((prevPage) => Math.min(totalPages - 1, prevPage + 1));
};
