import { useState } from "react";
import SignUpForm from "../components/SignUpForm";
import ProfileForm from "../components/ProfileForm";
import { submitHandlerSignUp } from "../functions/signUpPageFunctions";

const SignUpPage = ({ onSignUp }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConf, setPasswordConf] = useState("");
  const [receivedData, setReceivedData] = useState();
  const [isSignUp, setIsSignUp] = useState(false);

  const loginHandler = () => {
    onSignUp[0](true);
  };

  return !isSignUp ? (
    <SignUpForm
      username={username}
      password={password}
      passwordConf={passwordConf}
      receivedData={receivedData}
      setUsername={setUsername}
      setPassword={setPassword}
      setPasswordConf={setPasswordConf}
      submitHandler={(event) =>
        submitHandlerSignUp(
          event,
          onSignUp,
          setReceivedData,
          setIsSignUp,
          username
        )
      }
      loginHandler={loginHandler}
    />
  ) : (
    <ProfileForm
      genres={receivedData.genres}
      actors={receivedData.actors}
      userId={receivedData.user_id}
      onCreateProfile={onSignUp[1]}
      username={username}
    />
  );
};

export default SignUpPage;
