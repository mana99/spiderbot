
USE fantacalcio;

-- Voti leggibile
CREATE OR REPLACE VIEW voti AS
SELECT nome, ruolo, squadra, giornata, voto, gol, assist, autogol, ammonizione, espulsione, rigore, rigore_sbagliato, fantavoto
FROM Votes join Player
where Votes.id = Player.id;

-- Cannonieri
CREATE OR REPLACE VIEW cannonieri AS
SELECT nome, SUM(gol) AS gol, COUNT(*) as presenze, AVG(voto) AS media_voto 
FROM Votes join Player on (Votes.id = Player.id)
GROUP BY nome
HAVING SUM(gol)>0
ORDER BY gol DESC;

-- Gol fatti e subiti per squadra
CREATE OR REPLACE VIEW gol_fatti_squadra AS
SELECT squadra, SUM(gol) AS gol_fatti
FROM Votes join Player on (Votes.id = Player.id)
WHERE ruolo != 'Por'
GROUP BY squadra
ORDER BY gol_fatti DESC;

CREATE OR REPLACE VIEW gol_subiti_squadra AS
SELECT squadra, SUM(gol) AS gol_subiti
FROM Votes join Player on (Votes.id = Player.id)
WHERE ruolo = 'Por'
GROUP BY squadra
ORDER BY gol_subiti DESC;

CREATE OR REPLACE VIEW differenza_reti AS
SELECT gol_fatti_squadra.squadra, gol_fatti, gol_subiti, gol_fatti + gol_subiti as differenza_reti 
FROM gol_fatti_squadra join gol_subiti_squadra on gol_fatti_squadra.squadra = gol_subiti_squadra.squadra
ORDER BY differenza_reti DESC;

-- Trasferimenti
CREATE OR REPLACE VIEW trasferimenti AS
SELECT nome, squadra, min(giornata) AS prima_giornata
FROM Votes join Player on (Votes.id = Player.id)
WHERE nome in (
	SELECT nome FROM fantacalcio.Player
	GROUP BY nome
	HAVING COUNT(*)>1
    )
GROUP BY nome, squadra
ORDER BY nome, prima_giornata;
