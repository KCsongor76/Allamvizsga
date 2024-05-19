// SignUpPage.js
export const submitHandlerSignUp = (
    event,
    onSignUp,
    setReceivedData,
    setIsSignUp
  ) => {
    event.preventDefault();
    const form = event.target;
  
    fetch(form.action, {
      method: "POST",
      body: new URLSearchParams(new FormData(form)),
    })
      .then((response) => response.json())
      .then((data) => {
        onSignUp[1](data);
        setReceivedData(data);
        if (data.actors && data.genres) {
          setIsSignUp(true);
        }
      })
      .catch((error) => console.error("Error:", error));
  };