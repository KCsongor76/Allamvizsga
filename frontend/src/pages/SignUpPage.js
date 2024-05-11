import { useState } from "react";
import classes from "./LoginPage.module.css";

const SignUpPage = ({ onAuth, onSignUp }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConf, setPasswordConf] = useState("");
  const [receivedData, setReceivedData] = useState();

  const submitHandler = (event) => {
    event.preventDefault();
    const form = event.target;

    fetch(form.action, {
      method: "POST",
      body: new URLSearchParams(new FormData(form)),
    })
      .then((response) => response.json())
      .then((data) => {
        onAuth(data);
        setReceivedData(data);
      })
      .catch((error) => console.error("Error:", error));
  };

  const loginHandler = () => {
    onSignUp(true);
  };

  return (
    <>
      <form
        action="/signup"
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
        <label className={classes.label}>
          Confirm Password
          <input
            type="password"
            id="password_confirmation"
            name="password_confirmation"
            value={passwordConf}
            onChange={(event) => setPasswordConf(event.target.value)}
            className={classes.input}
          />
        </label>
        <button type="submit" className={classes.button}>
          Sign Up
        </button>
        {receivedData && (
          <p className={classes.errorMessage}>{receivedData.message}</p>
        )}
      </form>
      <button className={classes.button} onClick={loginHandler}>
        Log in here
      </button>
    </>
  );
};

export default SignUpPage;
