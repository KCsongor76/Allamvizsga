import { Outlet } from "react-router-dom";
import MainNavigation from "../components/MainNavigation";

const RootLayout = ({ onAuth }) => {
  return (
    <>
      <MainNavigation onAuth={onAuth} />
      <main>
        <Outlet />
      </main>
    </>
  );
};

export default RootLayout;
