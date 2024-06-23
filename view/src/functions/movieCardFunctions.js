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
            movie: item,
            rating: data.rating, // Use the updated rating here
            isProfile: isProfile,
          },
        });
      } else {
        // If there's no rating data, navigate without updating rating
        navigate(`${index}`, {
          state: {
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
