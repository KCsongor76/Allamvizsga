//Row.js
// Function to calculate items per page based on resolution
export const calculateItemsPerPage = () => {
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
