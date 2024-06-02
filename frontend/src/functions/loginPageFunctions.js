export const submitHandlerLogin = (
  event,
  onAuth,
  setReceivedData,
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
      onAuth({ ...data, username });
      setReceivedData(data);
    })
    .catch((error) => console.error("Error:", error));
};
