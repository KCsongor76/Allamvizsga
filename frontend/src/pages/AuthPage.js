import { useState } from "react";
import LoginPage from "./LoginPage";
import SignUpPage from "./SignUpPage";

const AuthPage = ({ onAuth, onSignUp, isLogin }) => {
  const [isLoginState, setIsLoginState] = useState(isLogin);
  
  return isLoginState ? (
    <LoginPage onAuth={onAuth} onLogin={setIsLoginState} />
  ) : (
    <SignUpPage onSignUp={[setIsLoginState, onSignUp]} />
  );
};

export default AuthPage;
