-- Active: 1680640168593@@127.0.0.1@3306@appointment
-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `appointment`
--
CREATE DATABASE IF NOT EXISTS `appointment` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `appointment`;

-- --------------------------------------------------------

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
CREATE TABLE IF NOT EXISTS `appointment` (
  `appointmentID` int(11) NOT NULL AUTO_INCREMENT,
  `doctorID` int(11) NOT NULL,
  `patientID` varchar(32) NOT NULL,
  `patientName` varchar(64) NOT NULL,
  `date` varchar(64) NOT NULL,
  `time` int(4) NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`appointmentID`))
  -- FOREIGN KEY (`doctorID`, `date`, `time`) REFERENCES `schedule` (`doctorID`, `date`, `time`)) 
  ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `appointment` (`appointmentID`, `doctorID`, `patientID`, `patientName`, `date`, `time`, `created`) VALUES
(1, 1, '516A', 'Jane Tan', '2023-05-01', 1100, '2023-04-05 02:14:55'),
(2, 2, '823B', 'Timothy Wong', '2023-05-02', 1400, '2023-04-06 12:47:12');

select * from appointment;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
