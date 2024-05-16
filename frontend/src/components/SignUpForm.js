import classes from "../pages/LoginPage.module.css";

const SignUpForm = ({
  username,
  password,
  passwordConf,
  receivedData,
  setUsername,
  setPassword,
  setPasswordConf,
  submitHandler,
  loginHandler,
}) => {
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

export default SignUpForm;
