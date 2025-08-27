# Newspaper Database (Chronicling America, 18th Century)

## Project Overview

This project builds a relational database from Chronicling America’s digitized newspapers, focusing on the **people and institutions behind print culture in early America**.  
The database captures the **relationships between printers, their families, newspapers, political affiliations, publication geography, and the occurrence of key terms (e.g., "tyranny")**, with issues and pages serving as the structural backbone.  

The goal is to make visible how networks of printers — such as the Franklin family and their associates — shaped the circulation of news, ideas, and political discourse.

---

## Data Model Summary

### Entities and Relationships

- **PRINTER**: Represents an individual printer or publisher. Includes biographical information (lifespan, place of activity, notes), **political affiliation**, and **family connections**.  
- **PRINTER_RELATIONSHIP**: Captures ties between printers, such as **family ties (e.g., uncle/niece, father/son)** or **apprenticeship/mentorship**.  
- **NEWSPAPER**: Each newspaper is associated with one or more printers across its lifespan. Includes title, place, start/end years, and associated printer(s).  
- **ISSUE**: Each issue belongs to one newspaper and represents a specific publication date. Includes publication date, volume, issue number, and **count of "tyranny" mentions**.  
- **PAGE**: Each page belongs to one issue. Provides page-level metadata (page number).  

---

### ER Diagram (ASCII Art)

[PRINTER]---<publishes>---{NEWSPAPER}---<contains>---{ISSUE}---<has>---{PAGE}
|
|<--related_to-->{PRINTER_RELATIONSHIP}

PRINTER
+------------------+
| printer_id PK |
| name |
| lifespan |
| affiliation |
| political_view |
| notes |
+------------------+

PRINTER_RELATIONSHIP
+------------------+
| rel_id PK |
| printer1_id FK |
| printer2_id FK |
| relationship | (e.g., "brother", "apprentice", "business partner")
+------------------+

NEWSPAPER
+------------------+
| newspaper_id PK |
| title |
| place |
| start_year |
| end_year |
| printer_id FK |
+------------------+

ISSUE
+-------------------------+
| issue_id PK |
| newspaper_id FK |
| pub_date DATE |
| volume_number |
| issue_number |
| tyranny_mentions_count |
+-------------------------+

PAGE
+------------------+
| page_id PK |
| issue_id FK |
| page_number |
+------------------+


---

### SQL Schema

```sql
CREATE TABLE PRINTER (
    printer_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    lifespan VARCHAR(255),
    affiliation VARCHAR(255),
    political_view VARCHAR(255),
    notes TEXT
);

CREATE TABLE PRINTER_RELATIONSHIP (
    rel_id INTEGER PRIMARY KEY,
    printer1_id INTEGER NOT NULL,
    printer2_id INTEGER NOT NULL,
    relationship VARCHAR(100),
    FOREIGN KEY (printer1_id) REFERENCES PRINTER(printer_id),
    FOREIGN KEY (printer2_id) REFERENCES PRINTER(printer_id)
);

CREATE TABLE NEWSPAPER (
    newspaper_id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    place VARCHAR(255),
    start_year INTEGER,
    end_year INTEGER,
    printer_id INTEGER,
    FOREIGN KEY (printer_id) REFERENCES PRINTER(printer_id)
);

CREATE TABLE ISSUE (
    issue_id INTEGER PRIMARY KEY,
    newspaper_id INTEGER,
    pub_date DATE,
    volume_number VARCHAR(50),
    issue_number VARCHAR(50),
    tyranny_mentions_count INTEGER DEFAULT 0,
    FOREIGN KEY (newspaper_id) REFERENCES NEWSPAPER(newspaper_id)
);

CREATE TABLE PAGE (
    page_id INTEGER PRIMARY KEY,
    issue_id INTEGER,
    page_number INTEGER,
    FOREIGN KEY (issue_id) REFERENCES ISSUE(issue_id)
);



