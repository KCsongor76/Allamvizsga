import { useState } from "react";
import SignUpForm from "../components/SignUpForm";
import ProfileForm from "../components/ProfileForm";

const SignUpPage = ({ onSignUp }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConf, setPasswordConf] = useState("");
  const [receivedData, setReceivedData] = useState();

  const [isSignUp, setIsSignUp] = useState(false);

  const submitHandler = (event) => {
    event.preventDefault();
    const form = event.target;

    fetch(form.action, {
      method: "POST",
      body: new URLSearchParams(new FormData(form)),
    })
      .then((response) => response.json())
      .then((data) => {
        onSignUp[1](data);
        setReceivedData(data);
        if (data.actors && data.genres) {
          setIsSignUp(true);
        }
      })
      .catch((error) => console.error("Error:", error));
  };

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
      submitHandler={submitHandler}
      loginHandler={loginHandler}
    />
  ) : (
    <ProfileForm
      genres={receivedData.genres}
      actors={receivedData.actors}
      onCreateProfile={onSignUp[1]}
    />
  );
};

export default SignUpPage;
