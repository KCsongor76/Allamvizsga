export const submitHandlerSignUp = (
  event,
  onSignUp,
  setReceivedData,
  setIsSignUp,
  username
) => {
  event.preventDefault();
  const form = event.target;

  fetch(form.action, {
    method: "POST",
    body: new URLSearchParams(new FormData(form)),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log({ ...data, username });
      onSignUp[1]({ ...data, username });
      setReceivedData({ ...data, username });
      if (data.actors && data.genres) {
        setIsSignUp(true);
      }
    })
    .catch((error) => console.error("Error:", error));
};
