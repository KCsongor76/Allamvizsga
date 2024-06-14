// MovieComponent.js
export const navigateHandler = (
  index,
  username,
  userId,
  item,
  isProfile,
  navigate
) => {
  const requestData = {
    userId: userId,
    movieId: item.id,
  };
  // Send a POST request to the Flask backend
  fetch("/get_rating_by_ids", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestData),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json(); // Assuming the response is JSON
    })
    .then((data) => {
      // Handle the response data if needed
      console.log("Response from backend, rating:", data);
      if (data.rating) {
        navigate(`/${index}`, {
          state: {
            //username: username,
            //userId: userId,
            movie: item,
            rating: data.rating, // Use the updated rating here
            isProfile: isProfile,
          },
        });
      } else {
        // If there's no rating data, navigate without updating rating
        navigate(`${index}`, {
          state: {
            //username: username,
            //userId: userId,
            movie: item,
            isProfile: isProfile,
          },
        });
      }
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
};
