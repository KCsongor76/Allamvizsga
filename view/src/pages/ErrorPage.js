import {useNavigate} from "react-router-dom";

const ErrorPage = ({isAuth}) => {
    const navigate = useNavigate();

    const navigateHandler = () => {
        isAuth ? navigate("/main") : navigate("/");
    };

    return (
        <div style={{textAlign: "center"}}>
            <p>Something went wrong!</p>
            <p>To go back to the main page, click on the button below!</p>
            <button style={{padding: "10px"}} onClick={navigateHandler}>
                GO BACK
            </button>
        </div>
    );
};

export default ErrorPage;
