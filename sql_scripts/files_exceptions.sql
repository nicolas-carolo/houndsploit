# Last update: February 1, 2019

USE HOUNDSPLOIT;

DROP TABLE IF EXISTS searcher_suggestion;
CREATE TABLE searcher_suggestion(
	searched    		VARCHAR(50) NOT NULL,
	suggestion  		VARCHAR(50) NOT NULL,
	replace_searched	BOOLEAN NOT NULL		
);

INSERT INTO searcher_suggestion(searched, suggestion, replace_searched) VALUES ('Joomla', 'Joomla!', true);
INSERT INTO searcher_suggestion(searched, suggestion, replace_searched) VALUES ('Linux', 'Linux Kernel', false);
INSERT INTO searcher_suggestion(searched, suggestion, replace_searched) VALUES ('PHPBB', 'PNPHPBB2', false);
INSERT INTO searcher_suggestion(searched, suggestion, replace_searched) VALUES ('macOS', 'Mac OS X', false);
INSERT INTO searcher_suggestion(searched, suggestion, replace_searched) VALUES ('Mac OS X', 'macOS', false);

