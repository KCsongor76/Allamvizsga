export const submitHandlerLogin = (
  event,
  onAuth,
  setReceivedData,
  username,
  setLoading
) => {
  event.preventDefault();
  const form = event.target;
  setLoading(true);

  fetch(form.action, {
    method: "POST",
    body: new URLSearchParams(new FormData(form)),
  })
    .then((response) => response.json())
    .then((data) => {
      setLoading(false);
      onAuth({ ...data, username });
      setReceivedData(data);
    })
    .catch((error) => {
      setLoading(false);
      console.error("Error:", error);
    });
};
