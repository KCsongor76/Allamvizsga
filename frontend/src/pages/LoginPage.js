import { useState } from "react";
import classes from "./LoginPage.module.css";
import { submitHandlerLogin } from "../functions/loginPageFunctions";
import LabelInput from "../components/FormElements/LabelInput";

const LoginPage = ({ onAuth, onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [receivedData, setReceivedData] = useState();

  return (
    <>
      <form
        action="/login"
        method="POST"
        onSubmit={(event) => submitHandlerLogin(event, onAuth, setReceivedData, username)}
        className={classes.container}
      >
        <LabelInput
          labelText="Username"
          type="text"
          id="username"
          name="username"
          value={username}
          setter={setUsername}
        />

        <LabelInput
          labelText="Password"
          type="password"
          id="password"
          name="password"
          value={password}
          setter={setPassword}
        />

        <p className={classes.link} onClick={() => onLogin(false)}>
          Don't have an account yet? Sign up here!
        </p>
        <button type="submit" className={classes.button}>
          Login
        </button>
        {receivedData && (
          <p className={classes.errorMessage}>{receivedData.message}</p>
        )}
      </form>
    </>
  );
};

export default LoginPage;
