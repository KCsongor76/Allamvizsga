import classes from "./SignUpForm.module.css";
import LabelInput from "./FormElements/LabelInput";

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

        <LabelInput
          labelText="Confirm Password"
          type="password"
          id="password_confirmation"
          name="password_confirmation"
          value={passwordConf}
          setter={setPasswordConf}
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
