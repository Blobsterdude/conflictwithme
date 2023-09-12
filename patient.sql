CREATE DATABASE IF NOT EXISTS `patient` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `patient`;

DROP TABLE IF EXISTS `patient`;
CREATE TABLE IF NOT EXISTS `patient` (
  `patientID` varchar(64) NOT NULL,
  `patientName` varchar(64) NOT NULL,
  `dob` varchar(64) NOT NULL,
  `nric` varchar(9) NOT NULL,
  `addr` varchar(64) NOT NULL,
  `mobileno` varchar(64) NOT NULL,
  PRIMARY KEY (`patientID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `schedule`

INSERT INTO `patient` (`patientID`, `patientName`, `dob`, `nric`, `addr`, `mobileno`) VALUES
('456Z', 'James Ng', '2023-05-01', 'A123456Z', '30 Punggol Street', '91234567'),
('456X' , 'Spongebob', '2023-05-01', 'B123456X', '50 Pineapple Rd', '81234567');
-- Keeping mobile as string because might have symbols in numbers like "+" and space " "