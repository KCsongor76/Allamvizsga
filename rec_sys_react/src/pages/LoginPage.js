import {useState} from "react";
import classes from './LoginPage.module.css';

const LoginPage = ({onAuth}) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const [receivedData, setReceivedData] = useState();

    const submitHandler = (event) => {
        event.preventDefault();
        const form = event.target;

        fetch(form.action, {
            method: 'POST',
            body: new URLSearchParams(new FormData(form)),
        })
            .then(response => response.json())
            .then(data => {
                onAuth(data);
                setReceivedData(data);
            })
            .catch(error => console.error('Error:', error));
    }

    return (
        <form
            action="http://localhost:8000/testRecommendationSystem.php"
            method="POST"
            onSubmit={event => submitHandler(event)}
            className={classes.container}
        >
            <label className={classes.label}>
                Username
                <input
                    type="text"
                    id="username"
                    name="username"
                    value={username}
                    onChange={event => setUsername(event.target.value)}
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
                    onChange={event => setPassword(event.target.value)}
                    className={classes.input}
                />
            </label>
            <button type="submit" className={classes.button}>
                Login
            </button>
            {receivedData && <p className={classes.errorMessage}>{receivedData.message}</p>}
        </form>

    );
}

export default LoginPage;