## CSV Data Mapping

The file `alltyrannysimplified.csv` contains the raw data for this project. Each row represents a mention of "tyranny" in a newspaper page, with the following columns:

- **id**: URL to the newspaper page on Chronicling America. Can be used to identify the newspaper, issue, and page.
- **pub_date**: Publication date of the issue. Maps to `ISSUE.pub_date`.
- **text**: The context in which "tyranny" is mentioned. Maps to `MENTION.context_text`.
- **city**: City of publication. Helps describe the `NEWSPAPER` entity.
- **state**: State of publication. Helps describe the `NEWSPAPER` entity.
- **frequency**: Publication frequency (e.g., weekly, semiweekly). Maps to `NEWSPAPER` or can be stored as metadata.
- **page_number**: The page number within the issue. Maps to `PAGE.page_number`.

### Mapping Logic & Assumptions

- The URL (`id`) may encode information about the newspaper, issue, and page, but additional parsing or external lookup may be needed to fully populate all schema fields.
- If multiple cities or states are listed, the first or most prominent may be used for the `NEWSPAPER` entity.
- Each row is treated as a unique mention, even if multiple mentions occur on the same page.
- Additional fields (e.g., volume, issue number, publisher) may need to be inferred or supplemented from external sources if not present in the CSV.

This mapping ensures that the CSV data can be imported into the relational schema for further analysis and research.
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


