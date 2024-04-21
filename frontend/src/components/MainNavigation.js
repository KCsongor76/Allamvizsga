import {NavLink} from "react-router-dom";
import classes from "./MainNavigation.module.css";

const MainNavigation = ({onAuth}) => {
    return (
        <nav className={classes.container}>
            <ul className={classes.navList}>
                <li>
                    <NavLink to="/" className={classes.navLink}>
                        Main
                    </NavLink>
                </li>
                <li>
                    <NavLink to="/" onClick={() => onAuth(false)} className={classes.navLink}>
                        Log Out
                    </NavLink>
                </li>
            </ul>
        </nav>
    );
};

export default MainNavigation;
