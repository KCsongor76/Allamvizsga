import React, { useContext } from "react";
import { UserContext } from "../App";
import { useLoaderData } from "react-router-dom";
import ProfileDataComponent from "./ProfileDataComponent";
import ProfilePageRow from "./ProfilePageRow";

const MyProfilePage = () => {
  const { username } = useContext(UserContext);
  const userStats = useLoaderData();
  console.log(username);

  return (
    <>
      <ProfileDataComponent userStats={userStats} />
      {userStats.movies && <ProfilePageRow movies={userStats.movies} isProfile={true} />}
    </>
  );
};

export default MyProfilePage;
