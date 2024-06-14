// MainPage.js
export const getUsernameById = (userId, setUsername) => {
  const requestData = {
    userId: userId,
  };
  // Send a POST request to the Flask backend
  fetch("/get_username_by_id", {
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
      return response.json();
    })
    .then((data) => {
      console.log("getUsernameById exec");
      setUsername(data.username);
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
};
