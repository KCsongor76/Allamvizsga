import { useState } from "react";
import classes from "./LoginPage.module.css";

const LoginPage = ({ onAuth, onSignUp }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [receivedData, setReceivedData] = useState();

  const submitHandler = (event) => {
    event.preventDefault();
    const form = event.target;

    fetch(form.action, {
      method: "POST",
      body: new URLSearchParams(new FormData(form)),
    })
      .then((response) => {
        console.log(response.status);
        return response.json();
      })
      .then((data) => {
        console.log(data);
        onAuth(data);
        setReceivedData(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const signUpHandler = (event) => {
    //console.log(event.target);
    onSignUp(false);
  };

  return (
    <>
      <form
        action="/login"
        method="POST"
        onSubmit={(event) => submitHandler(event)}
        className={classes.container}
      >
        <label className={classes.label}>
          Username
          <input
            type="text"
            id="username"
            name="username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            className={classes.input}
          />
        </label>

        <label className={classes.label}>
          Password
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            className={classes.input}
          />
        </label>
        <button type="submit" className={classes.button}>
          Login
        </button>
        {receivedData && (
          <p className={classes.errorMessage}>{receivedData.message}</p>
        )}
      </form>
      <button className={classes.button} onClick={signUpHandler}>
        Sign up here
      </button>
    </>
  );
};

export default LoginPage;
