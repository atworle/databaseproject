# Newspaper Tyranny Mentions Database (Chronicling America 1730-1783)

## Project Overview

This project contains a relational database built from the Chronicling America database, specifically focused on every newspaper page that mentions "tyranny" from 1730 to 1783. The data model is designed to capture the relationships between publishers, newspapers, issues, pages, and individual mentions of tyranny. The schema below is intended to support historical research, text analysis, and exploration of the context in which tyranny was discussed in early American newspapers.


## Data Model Summary

### Entities and Relationships

- **PUBLISHER**: Each publisher can publish multiple newspapers. Includes name, lifespan, affiliation, and notes.
- **NEWSPAPER**: Each newspaper is published by one publisher and can have multiple issues. Includes title, place, years, and publisher reference.
- **ISSUE**: Each issue belongs to one newspaper and can have multiple pages. Includes publication date, volume, and issue number.
- **PAGE**: Each page belongs to one issue and can include multiple mentions. Includes page number and issue reference.
- **MENTION**: Each mention is associated with one page and represents a specific instance of "tyranny" being mentioned. Includes context text, column/line, and position in text.


### ER Diagram (ASCII Art)

```
[PUBLISHER]---<publishes>---{NEWSPAPER}---<contains>---{ISSUE}---<has>---{PAGE}---<includes>---{MENTION}

PUBLISHER
+------------------+
| publisher_id PK  |
| name             |
| lifespan         |
| affiliation      |
| notes            |
+------------------+

NEWSPAPER
+------------------+
| newspaper_id PK  |
| title            |
| place            |
| start_year       |
| end_year         |
| publisher_id FK  |
+------------------+

ISSUE
+------------------+
| issue_id PK      |
| newspaper_id FK  |
| pub_date         |
| volume_number    |
| issue_number     |
+------------------+

PAGE
+------------------+
| page_id PK       |
| issue_id FK      |
| page_number      |
+------------------+

MENTION
+------------------+
| mention_id PK    |
| page_id FK       |
| context_text     |
| column_line      |
| position_in_text |
+------------------+
```


### SQL Schema

```sql
CREATE TABLE PUBLISHER (
    publisher_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    lifespan VARCHAR(255),
    affiliation VARCHAR(255),
    notes TEXT
);

CREATE TABLE NEWSPAPER (
    newspaper_id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    place VARCHAR(255),
    start_year INTEGER,
    end_year INTEGER,
    publisher_id INTEGER,
    FOREIGN KEY (publisher_id) REFERENCES PUBLISHER(publisher_id)
);

CREATE TABLE ISSUE (
    issue_id INTEGER PRIMARY KEY,
    newspaper_id INTEGER,
    pub_date DATE,
    volume_number VARCHAR(50),
    issue_number VARCHAR(50),
    FOREIGN KEY (newspaper_id) REFERENCES NEWSPAPER(newspaper_id)
);

CREATE TABLE PAGE (
    page_id INTEGER PRIMARY KEY,
    issue_id INTEGER,
    page_number INTEGER,
    FOREIGN KEY (issue_id) REFERENCES ISSUE(issue_id)
);

CREATE TABLE MENTION (
    mention_id INTEGER PRIMARY KEY,
    page_id INTEGER,
    context_text TEXT,
    column_line VARCHAR(50),
    position_in_text INTEGER,
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id)
);
```

---

**Note:** For a graphical ER diagram, consider using tools like dbdiagram.io or draw.io to visualize the schema. If you need to extend the schema to include additional metadata or relationships, you can add new tables or fields as needed for your research.
