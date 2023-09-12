-- Active: 1680640168593@@127.0.0.1@3306@medicine
CREATE DATABASE IF NOT EXISTS `medicine` DEFAULT CHARACTER SET utf8 collate utf8_general_ci;
USE `medicine`;

DROP TABLE IF EXISTS medicine_inventory;

CREATE TABLE IF NOT EXISTS medicine_inventory (
  medicineName varchar(32) NOT NULL,
  quantity int(8) NOT NULL,
  lowStock BIT(1) NOT NULL,
  PRIMARY KEY (`medicineName`)
) ENGINE=InnoDB;


INSERT INTO medicine_inventory (medicineName, quantity, lowStock)
VALUES ('Medicine A', 1, 0);
INSERT INTO medicine_inventory (medicineName, quantity, lowStock)
VALUES ('Medicine B', 1, 0);
INSERT INTO medicine_inventory (medicineName, quantity, lowStock)
VALUES ('Medicine C', 1, 0);
INSERT INTO medicine_inventory (medicineName, quantity, lowStock)
VALUES ('Medicine D', 1, 0);
SELECT * FROM medicine_inventory;
