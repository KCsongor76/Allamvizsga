import React from "react";
import { useLoaderData } from "react-router-dom";
import ProfileDataComponent from "./ProfileDataComponent";
import ProfilePageRow from "./ProfilePageRow";

const MyProfilePage = () => {
  const userStats = useLoaderData();

  return (
    <>
      <ProfileDataComponent userStats={userStats} />
      {userStats.movies && <ProfilePageRow movies={userStats.movies} isProfile={true} />}
    </>
  );
};

export default MyProfilePage;
