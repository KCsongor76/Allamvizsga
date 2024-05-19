export const submitHandlerLogin = (event, onAuth, setReceivedData) => {
  event.preventDefault();
  const form = event.target;

  fetch(form.action, {
    method: "POST",
    body: new URLSearchParams(new FormData(form)),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      onAuth(data);
      setReceivedData(data);
      console.log("login handler executed")
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};
