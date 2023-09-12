-- Active: 1680640168593@@127.0.0.1@3306@queue
CREATE DATABASE IF NOT EXISTS `queue` DEFAULT CHARACTER SET utf8 collate utf8_general_ci;
USE `queue`;

DROP TABLE IF EXISTS queue;
DROP TABLE IF EXISTS medicine_inventory;
CREATE TABLE IF NOT EXISTS queue (
  patientId VARCHAR(4) NOT NULL,
  medicineNeeded JSON NOT NULL,
  is_served int(7) NOT NULL,
  PRIMARY KEY (`patientId`)
) ENGINE=InnoDB;

INSERT INTO queue (patientId, medicineNeeded, is_served)
VALUES ('042A', '{"medicine":[{"name":"Medicine A", "quantity":2}]}', 0);
INSERT INTO queue (patientId, medicineNeeded, is_served)
VALUES ('049B', '{"medicine":[{"name":"Medicine A", "quantity":2}]}', 0);

select * from queue