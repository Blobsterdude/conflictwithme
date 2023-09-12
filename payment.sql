
CREATE DATABASE IF NOT EXISTS `payment` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `payment`;

-- DROP TABLE IF EXISTS patient;
-- CREATE TABLE IF NOT EXISTS patient (
--   patientID int(7) NOT NULL,
--   pName varchar(32) NOT NULL,
--   pAddress varchar(1000) NOT NULL,
--   pPhone int(8) NOT NULL,
--   PRIMARY KEY (`patientId`)
-- ) ENGINE=InnoDB;

-- INSERT INTO patient (patientID, pName, pAddress, pPhone) VALUES
-- (1234560, 'John Tan', '123 Happy Road', '81234567'),
-- (1234567, 'Amy Teo', '76 ABC Road', '83456789'),
-- (6789012, 'Lee Tan', '89 XYZ Road','86789345');

DROP TABLE IF EXISTS `payment`;
CREATE TABLE IF NOT EXISTS `payment` (
    `invoiceNo` INT NOT NULL,
    `paymentStatus` VARCHAR(50) NOT NULL,
    `patientID` VARCHAR(4) NOT NULL,
    `payDate` DATE NOT NULL,
    `amount` FLOAT,
    PRIMARY KEY (`invoiceNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `payment` (`invoiceNo`, `paymentStatus`, `patientID`, `payDate`, `amount`) VALUES
(7654321, 'Paid', '048A', '2022-08-27','39.40'),
(9876540, 'Unpaid', '051A', '2023-02-28', '80.20'),
(4567890, 'Unpaid','048A','2022-09-23','25.30'),
(8887765, 'Unpaid', '048A', '2022-03-17','90.40'),
(8287005, 'Paid', '048A', '2022-09-08','100.90');

select * from payment
