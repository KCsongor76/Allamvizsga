import { NavLink } from "react-router-dom";
import classes from "./MainNavigation.module.css";
import { useContext } from "react";
import { UserContext } from "../App";

const MainNavigation = ({ onAuth }) => {
  const { username } = useContext(UserContext);


  return (
    <nav className={classes.container}>
      <ul className={classes.navList}>
        <li>
          <NavLink to="/" className={classes.navLink}>
            Main
          </NavLink>
        </li>
        <li>
          <NavLink to={`/users/${username}`} className={classes.navLink}>
            My Profile
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/"
            onClick={() => onAuth(false)}
            className={classes.navLink}
          >
            Log Out
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default MainNavigation;
