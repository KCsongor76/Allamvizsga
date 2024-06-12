import classes from "./SignUpForm.module.css";

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

        <label className={classes.label}>Confirm Password</label>
        <input
          className={classes.input}
          type="password"
          id="password_confirmation"
          name="password_confirmation"
          value={passwordConf}
          onChange={(event) => setPasswordConf(event.target.value)}
        />

        <p className={classes.link} onClick={loginHandler}>
          Already have an account? Log in here!
        </p>
        <button type="submit" className={classes.button}>
          Sign Up
        </button>
        {receivedData && (
          <p className={classes.errorMessage}>{receivedData.message}</p>
        )}
      </form>
    </>
  );
};

export default SignUpForm;
