import { useState } from "react";
import classes from "./LoginPage.module.css";
import { submitHandlerLogin } from "../functions/loginPageFunctions";

const LoginPage = ({ onAuth, onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [receivedData, setReceivedData] = useState();
  const [loading, setLoading] = useState(false);

  return (
    <>
      <form
        action="/login"
        method="POST"
        onSubmit={(event) =>
          submitHandlerLogin(
            event,
            onAuth,
            setReceivedData,
            username,
            setLoading
          )
        }
        className={classes.container}
      >
        <label className={classes.label}>Username</label>
        <input
          className={classes.input}
          type="text"
          id="username"
          name="username"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
        />

        <label className={classes.label}>Password</label>
        <input
          className={classes.input}
          type="password"
          id="password"
          name="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />

        <p className={classes.link} onClick={() => onLogin(false)}>
          Don't have an account yet? Sign up here!
        </p>
        <button type="submit" className={classes.button}>
          Login
        </button>
        {receivedData && !loading && (
          <p className={classes.errorMessage}>{receivedData.message}</p>
        )}
        {loading && <div className={classes.loadingIcon} />}
      </form>
    </>
  );
};

export default LoginPage;
