# Last update: February 5, 2019

USE HOUNDSPLOIT;

DROP TABLE IF EXISTS searcher_suggestion;
CREATE TABLE searcher_suggestion(
	id					INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	searched    		VARCHAR(50) NOT NULL UNIQUE,
	suggestion  		VARCHAR(50) NOT NULL,
	autoreplacement		BOOLEAN NOT NULL	
);

INSERT INTO searcher_suggestion(searched, suggestion, autoreplacement) VALUES ('joomla', 'joomla!', true);
INSERT INTO searcher_suggestion(searched, suggestion, autoreplacement) VALUES ('linux', 'linux kernel', false);
INSERT INTO searcher_suggestion(searched, suggestion, autoreplacement) VALUES ('phpbb', 'pnphpbb2', false);
INSERT INTO searcher_suggestion(searched, suggestion, autoreplacement) VALUES ('macos', 'mac os x', false);
INSERT INTO searcher_suggestion(searched, suggestion, autoreplacement) VALUES ('mac os x', 'macos', false);
INSERT INTO searcher_suggestion(searched, suggestion, autoreplacement) VALUES ('html 5', 'html5', true);
