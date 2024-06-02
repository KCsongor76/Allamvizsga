import React, { useContext } from "react";
import { UserContext } from "../App";
import Row from "./Row";
import { useLoaderData } from "react-router-dom";
import ProfileDataComponent from "./ProfileDataComponent";

const MyProfilePage = () => {
  const { username } = useContext(UserContext);
  const userStats = useLoaderData();
  console.log(username);

  return (
    <>
      <ProfileDataComponent userStats={userStats} />
      {userStats.movies && <Row movies={userStats.movies} isProfile={true} />}
    </>
  );
};

export default MyProfilePage;
