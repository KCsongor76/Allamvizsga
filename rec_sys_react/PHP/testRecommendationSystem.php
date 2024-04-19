<?php
include_once '../../RecSysPhp/RecSys/RecommendationSystem.php';

header('Access-Control-Allow-Origin: http://localhost:3001');
header('Content-Type: application/json');

$username = $_POST["username"];
$password = $_POST["password"];

$result = RecommendationSystem::checkLogin($username, $password);
print_r($result);
