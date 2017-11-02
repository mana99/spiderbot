
CREATE DATABASE fantacalcio;

CREATE USER 'fantauser'@'localhost' IDENTIFIED BY 'calciofanta';
GRANT ALL PRIVILEGES ON fantacalcio . * TO 'fantauser'@'localhost' identified by 'calciofanta';
FLUSH PRIVILEGES;

-- User for automation with airflow
CREATE USER 'airflow'@'localhost';
GRANT ALL PRIVILEGES ON fantacalcio . * TO 'airflow'@'localhost';
FLUSH PRIVILEGES;

USE fantacalcio;

DROP TABLE IF EXISTS `fantacalcio`.`fantatable`;
CREATE TABLE `fantacalcio`.`fantatable` (
  `guid` VARCHAR(45) NOT NULL,  -- guid = md5(nome+giornata+stagione)
  `nome` VARCHAR(45) NOT NULL,
  `numero` VARCHAR(45) NOT NULL,
  `ruolo` VARCHAR(45) NOT NULL,
  `squadra` VARCHAR(45) NOT NULL,
  `stagione` VARCHAR(45) NOT NULL,
  `giornata` VARCHAR(45) NOT NULL,
  `voto` VARCHAR(45) NOT NULL,
  `gol` VARCHAR(45) NOT NULL,
  `assist` VARCHAR(45) NOT NULL,
  `rigore` VARCHAR(45) NOT NULL,
  `rigore_sbagliato` VARCHAR(45) NOT NULL,
  `autogol` VARCHAR(45) NOT NULL,
  `ammonizione` VARCHAR(45) NOT NULL,
  `espulsione` VARCHAR(45) NOT NULL,
  `fantavoto` VARCHAR(45) NOT NULL,
  `updated` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`guid`) );
