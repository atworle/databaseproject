Newspaper Database (Chronicling America, 18th Century)
Project Overview

This project builds a relational database from Chronicling America’s digitized newspapers, focusing on the people and institutions behind print culture in early America (18th century).

The database is designed for historical research into printer networks, family dynasties, apprenticeships, and political discourse, with particular attention to the circulation of the word “tyranny.”

By linking biographical data, newspaper metadata, and textual mentions, the database enables analysis of who printed what, when, and where certain ideas appeared, while preserving relationships between printers and newspapers.

Data Model Summary

The database is structured around four main tables:

PRINTER

Biographical data for printers or publishers

Political affiliation, notes, and source citations

PRINTER_RELATIONSHIP

Family ties, apprenticeships, or business partnerships

Each relationship references two printers and a source

NEWSPAPER

Newspaper metadata (title, location, start/end years)

Links to printers via foreign key

MENTIONS

Each row is a single occurrence of the word “tyranny”

Includes date, page, issue, and newspaper reference

Optionally stores URL or snippet of the mention

All tables are linked via foreign keys, ensuring relational integrity.

Entity–Relationship Diagram (ASCII)
[PRINTER]---<publishes>---{NEWSPAPER}---<contains>---{MENTIONS}
   |
   |<--related_to-->{PRINTER_RELATIONSHIP}

Tables
PRINTER
Field	Type	Description
printer_id (PK)	INTEGER	Unique identifier
name	TEXT	Printer’s full name
lifespan	TEXT	Birth–death years
affiliation	TEXT	Institutional/family affiliation
political_view	TEXT	Political leaning
notes	TEXT	Additional notes
source_id (FK)	INTEGER	Citation for biographical info
PRINTER_RELATIONSHIP
Field	Type	Description
rel_id (PK)	INTEGER	Unique relationship ID
printer1_id (FK)	INTEGER	First printer
printer2_id (FK)	INTEGER	Second printer
relationship	TEXT	Type (e.g., apprentice, brother, partner)
source_id (FK)	INTEGER	Citation for relationship
NEWSPAPER
Field	Type	Description
newspaper_id (PK)	INTEGER	Unique ID
title	TEXT	Newspaper title
place	TEXT	City/colony of publication
start_year	INTEGER	Earliest year
end_year	INTEGER	Latest year
printer_id (FK)	INTEGER	Linked printer
source_id (FK)	INTEGER	Citation for newspaper info
MENTIONS
Field	Type	Description
mention_id (PK)	INTEGER	Unique mention ID
newspaper_id (FK)	INTEGER	Newspaper reference
date	DATE	Publication date
issue_number	TEXT	Issue number
page_number	INTEGER	Page number
context	TEXT	Snippet or quote
url	TEXT	Page URL
SOURCES
Field	Type	Description
source_id (PK)	INTEGER	Unique ID
full_citation	TEXT	Full Chicago-style citation
short_citation	TEXT	Short form for quick reference
type	TEXT	Book, article, archive, etc.
SQL Schema Example
CREATE TABLE PRINTER (
    printer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    lifespan TEXT,
    affiliation TEXT,
    political_view TEXT,
    notes TEXT,
    source_id INTEGER
);

CREATE TABLE PRINTER_RELATIONSHIP (
    rel_id INTEGER PRIMARY KEY,
    printer1_id INTEGER NOT NULL,
    printer2_id INTEGER NOT NULL,
    relationship TEXT,
    source_id INTEGER,
    FOREIGN KEY (printer1_id) REFERENCES PRINTER(printer_id),
    FOREIGN KEY (printer2_id) REFERENCES PRINTER(printer_id),
    FOREIGN KEY (source_id) REFERENCES SOURCES(source_id)
);

CREATE TABLE NEWSPAPER (
    newspaper_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    place TEXT,
    start_year INTEGER,
    end_year INTEGER,
    printer_id INTEGER,
    source_id INTEGER,
    FOREIGN KEY (printer_id) REFERENCES PRINTER(printer_id),
    FOREIGN KEY (source_id) REFERENCES SOURCES(source_id)
);

CREATE TABLE MENTIONS (
    mention_id INTEGER PRIMARY KEY,
    newspaper_id INTEGER,
    date DATE,
    issue_number TEXT,
    page_number INTEGER,
    context TEXT,
    url TEXT,
    FOREIGN KEY (newspaper_id) REFERENCES NEWSPAPER(newspaper_id)
);

CREATE TABLE SOURCES (
    source_id INTEGER PRIMARY KEY,
    full_citation TEXT,
    short_citation TEXT,
    type TEXT
);



