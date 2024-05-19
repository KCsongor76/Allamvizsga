import { useState } from "react";
import classes from "./LoginPage.module.css";
import { submitHandlerLogin } from "../functions/loginPageFunctions";

const LoginPage = ({ onAuth, onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [receivedData, setReceivedData] = useState();

  return (
    <>
      <form
        action="/login"
        method="POST"
        onSubmit={(event) => submitHandlerLogin(event, onAuth, setReceivedData)}
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
      <button className={classes.button} onClick={() => onLogin(false)}>
        Sign up here
      </button>
    </>
  );
};

export default LoginPage;
