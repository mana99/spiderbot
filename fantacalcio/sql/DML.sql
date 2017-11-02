
USE fantacalcio;

-- Pulizia dati
UPDATE `fantacalcio`.`fantatable`
    SET gol=''
    WHERE gol = '-';
UPDATE `fantacalcio`.`fantatable`
    SET gol=''
    WHERE gol = '\r\n-		  ';
UPDATE `fantacalcio`.`fantatable`
    SET gol=''
    WHERE gol = '\r\n		  			-\r\n		  ';
UPDATE fantacalcio.fantatable SET gol = REPLACE(gol,'\n','');
UPDATE fantacalcio.fantatable SET gol = REPLACE(gol, '\t','');
UPDATE fantacalcio.fantatable SET gol = REPLACE(gol,'\r','');
UPDATE `fantacalcio`.`fantatable`
    SET assist=''
    WHERE assist = '-';
UPDATE `fantacalcio`.`fantatable`
    SET rigore=''
    WHERE rigore = '-';
UPDATE `fantacalcio`.`fantatable`
    SET autogol=''
    WHERE autogol = '-';
UPDATE `fantacalcio`.`fantatable`
    SET espulsione=''
    WHERE espulsione = '-'; 
UPDATE `fantacalcio`.`fantatable`
    SET ammonizione=''
    WHERE ammonizione = '-';  
UPDATE `fantacalcio`.`fantatable`
    SET rigore_sbagliato=''
    WHERE rigore_sbagliato = '-';
UPDATE `fantacalcio`.`fantatable`
	SET giornata=REPLACE(giornata,'^ giornata', '');

-- Creazione tabelle denormalizzate
DROP TABLE IF EXISTS Player;
CREATE TABLE Player
SELECT nome, squadra, ruolo, numero
FROM fantatable
GROUP BY nome, squadra;

ALTER TABLE `fantacalcio`.`Player` 
ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT AFTER `numero`,
ADD PRIMARY KEY (`id`);

DROP TABLE IF EXISTS Votes;
CREATE TABLE Votes
SELECT id, stagione, giornata, voto, gol, assist, autogol, ammonizione, espulsione, rigore, rigore_sbagliato, fantavoto
FROM fantatable join Player
on (fantatable.nome = Player.nome and fantatable.squadra = Player.squadra);
