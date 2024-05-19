import { NavLink } from "react-router-dom";
import classes from "./MainNavigation.module.css";
import { useContext, useEffect, useState } from "react";
import { UserContext } from "../App";
import { getUsernameById } from "../functions/mainPageFunctions";

const MainNavigation = ({ onAuth }) => {
  const userId = useContext(UserContext);
  const [username, setUsername] = useState("");
  console.log("MainNavigation");

  useEffect(() => {
    getUsernameById(userId, setUsername);
  }, [userId]);

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
