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
-- Database: `schedule`
--
CREATE DATABASE IF NOT EXISTS `schedule` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `schedule`;

-- --------------------------------------------------------

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
CREATE TABLE IF NOT EXISTS `schedule` (
  `doctorID` int(11) NOT NULL,
  `doctorName` varchar(64) NOT NULL,
  `date` varchar(64) NOT NULL,
  `time` int(4) NOT NULL,
  `available` boolean NOT NULL,
  PRIMARY KEY (`doctorID`, `date`, `time`)
  -- FOREIGN KEY (`appointmentID`) REFERENCES appointment(`appointmentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `schedule`
--

INSERT INTO `schedule` (`doctorID`, `doctorName`, `date`, `time`, `available`) VALUES
(1 , 'James Ng', '2023-05-01', 1000, 1),
(1 , 'James Ng', '2023-05-01', 1100, 1),
(1 , 'James Ng', '2023-05-01', 1300, 1),
(1 , 'James Ng', '2023-05-01', 1400, 1),
(1 , 'James Ng', '2023-05-01', 1500, 1),
(1 , 'James Ng', '2023-05-02', 1100, 1),
(1 , 'James Ng', '2023-05-02', 1300, 1),
(1 , 'James Ng', '2023-05-02', 1400, 1),
(1 , 'James Ng', '2023-05-02', 1500, 1),
(1 , 'James Ng', '2023-05-02', 1600, 1),
(2, 'Regine Tan', '2023-05-01', 1000, 1),
(2, 'Regine Tan', '2023-05-01', 1100, 1),
(2, 'Regine Tan', '2023-05-01', 1300, 1),
(2, 'Regine Tan', '2023-05-01', 1400, 1),
(2, 'Regine Tan', '2023-05-01', 1500, 1),
(2, 'Regine Tan', '2023-05-02', 1000, 1),
(2, 'Regine Tan', '2023-05-02', 1100, 1),
(2, 'Regine Tan', '2023-05-02', 1300, 1),
(2, 'Regine Tan', '2023-05-02', 1400, 1),
(2, 'Regine Tan', '2023-05-02', 1500, 1);

-- --------------------------------------------------------


-- Constraints for dumped tables
--

--
-- Constraints for table `order_item`
--

-- ALTER TABLE `appointment`
-- ADD FOREIGN KEY (`doctorID`, `date`, `time`) REFERENCES `schedule` (`doctorID`, `date`, `time`) ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ALTER TABLE `appointment`
--   ADD CONSTRAINT `FK_doctorID` FOREIGN KEY (`doctorID`) REFERENCES `schedule` (`doctorID`) ON DELETE CASCADE ON UPDATE CASCADE,
--   ADD CONSTRAINT `FK_date` FOREIGN KEY (`date`) REFERENCES `schedule` (`date`) ON DELETE CASCADE ON UPDATE CASCADE,
--   ADD CONSTRAINT `FK_time` FOREIGN KEY (`time`) REFERENCES `schedule` (`time`) ON DELETE CASCADE ON UPDATE CASCADE;
-- COMMIT;

-- select * from schedule
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
