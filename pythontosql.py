import csv
import sqlite3


try:
    conn = sqlite3.connect('printersv2.db')
    cur = conn.cursor()
    print("Connected to printersv2.db")
except sqlite3.Error as e:
    print(f"Error connecting to database: {e}")
    exit(1)


try:
    cur.execute("DROP TABLE IF EXISTS printers")
    cur.execute('''
    CREATE TABLE IF NOT EXISTS printers (
        printer_id INTEGER PRIMARY KEY,
        name TEXT,
        lifespan TEXT,
        affiliation TEXT,
        political_view TEXT,
        notes TEXT,
        source_id TEXT
    )
    ''')
    print("Created printers table")
except sqlite3.Error as e:
    print(f"Error creating printers table: {e}")
    conn.close()
    exit(1)


try:
    with open('printerbio.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  
        row_count = 0
        for row in reader:
            if len(row) != 7:
                print(f"Skipping invalid row in printerbio.csv: {row}")
                continue
            try:
                cur.execute('''
                INSERT INTO printers (printer_id, name, lifespan, affiliation, political_view, notes, source_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6]))
                row_count += 1
            except ValueError as e:
                print(f"Error inserting row in printerbio.csv: {row}, Error: {e}")
                continue
            except sqlite3.Error as e:
                print(f"Database error inserting row in printerbio.csv: {row}, Error: {e}")
                continue
        print(f"Inserted {row_count} rows into printers table")
except FileNotFoundError:
    print("Error: printerbio.csv not found")
    conn.close()
    exit(1)
except Exception as e:
    print(f"Unexpected error reading printerbio.csv: {e}")
    conn.close()
    exit(1)


try:
    cur.execute('''
    CREATE TABLE IF NOT EXISTS relationships (
        rel_id INTEGER PRIMARY KEY,
        printer1_id INTEGER,
        printer2_id INTEGER,
        relationship TEXT,
        source_id TEXT
    )
    ''')
    print("Created relationships table")
except sqlite3.Error as e:
    print(f"Error creating relationships table: {e}")
    conn.close()
    exit(1)


try:
    with open('printerrelationships.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  
        row_count = 0
        for row in reader:
            if len(row) != 5:
                print(f"Skipping invalid row in printerrelationships.csv: {row}")
                continue
            try:
                if not (row[0].isdigit() and row[1].isdigit() and row[2].isdigit()):
                    print(f"Skipping non-numeric ID row in printerrelationships.csv: {row}")
                    continue
                cur.execute('''
                INSERT INTO relationships (rel_id, printer1_id, printer2_id, relationship, source_id)
                VALUES (?, ?, ?, ?, ?)
                ''', (int(row[0]), int(row[1]), int(row[2]), row[3], row[4]))
                row_count += 1
            except ValueError as e:
                print(f"Error inserting row in printerrelationships.csv: {row}, Error: {e}")
                continue
            except sqlite3.Error as e:
                print(f"Database error inserting row in printerrelationships.csv: {row}, Error: {e}")
                continue
        print(f"Inserted {row_count} rows into relationships table")
except FileNotFoundError:
    print("Error: printerrelationships.csv not found")
    conn.close()
    exit(1)
except Exception as e:
    print(f"Unexpected error reading printerrelationships.csv: {e}")
    conn.close()
    exit(1)


try:
    cur.execute('''
    CREATE TABLE IF NOT EXISTS newspaper_series (
        series_id INTEGER PRIMARY KEY,
        canonical_name TEXT,
        notes TEXT
    )
    ''')
    print("Created newspaper_series table")
except sqlite3.Error as e:
    print(f"Error creating newspaper_series table: {e}")
    conn.close()
    exit(1)


try:
    with open('newspaper_series.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  
        row_count = 0
        for row in reader:
            if len(row) < 2 or len(row) > 3:
                print(f"Skipping invalid row in newspaper_series.csv: {row}")
                continue
            try:
                notes = row[2] if len(row) == 3 else ""
                cur.execute('''
                INSERT INTO newspaper_series (series_id, canonical_name, notes)
                VALUES (?, ?, ?)
                ''', (int(row[0]), row[1], notes))
                row_count += 1
            except ValueError as e:
                print(f"Error inserting row in newspaper_series.csv: {row}, Error: {e}")
                continue
            except sqlite3.Error as e:
                print(f"Database error inserting row in newspaper_series.csv: {row}, Error: {e}")
                continue
        print(f"Inserted {row_count} rows into newspaper_series table")
except FileNotFoundError:
    print("Error: newspaper_series.csv not found")
    conn.close()
    exit(1)
except Exception as e:
    print(f"Unexpected error reading newspaper_series.csv: {e}")
    conn.close()
    exit(1)


try:
    cur.execute("DROP TABLE IF EXISTS newspapers")
    cur.execute('''
    CREATE TABLE IF NOT EXISTS newspapers (
        newspaper_id INTEGER PRIMARY KEY,
        series_id INTEGER,
        title TEXT,
        start_year INTEGER,
        end_year INTEGER,
        place TEXT,
        printer_id INTEGER,
        FOREIGN KEY (series_id) REFERENCES newspaper_series(series_id),
        FOREIGN KEY (printer_id) REFERENCES printers(printer_id)
    );
    ''')
    print("Created newspapers table")
except sqlite3.Error as e:
    print(f"Error creating newspapers table: {e}")
    conn.close()
    exit(1)


try:
    with open('newspapers.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader) 
        row_count = 0
        for row in reader:
            if len(row) != 7:
                print(f"Skipping invalid row in newspapers.csv: {row}")
                continue
            try:
                cur.execute('''
                INSERT INTO newspapers (newspaper_id, series_id, title, start_year, end_year, place, printer_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (int(row[0]), int(row[1]), row[2], int(row[3]), int(row[4]), row[5], row[6]))
                row_count += 1
            except ValueError as e:
                print(f"Error inserting row in newspapers.csv: {row}, Error: {e}")
                continue
            except sqlite3.Error as e:
                print(f"Database error inserting row in newspapers.csv: {row}, Error: {e}")
                continue
        print(f"Inserted {row_count} rows into newspapers table")
except FileNotFoundError:
    print("Error: newspapers.csv not found")
    conn.close()
    exit(1)
except Exception as e:
    print(f"Unexpected error reading newspapers.csv: {e}")
    conn.close()
    exit(1)


try:
    cur.execute("DROP TABLE IF EXISTS tyranny_mentions")
    cur.execute('''
    CREATE TABLE IF NOT EXISTS tyranny_mentions (
        mention_id INTEGER PRIMARY KEY,
        newspaper_id INTEGER,
        aka TEXT,
        date TEXT,
        page_number INTEGER,
        partof_title TEXT,
        FOREIGN KEY (newspaper_id) REFERENCES newspapers(newspaper_id)
    )
    ''')
    print("Created tyranny_mentions table")
except sqlite3.Error as e:
    print(f"Error creating tyranny_mentions table: {e}")
    conn.close()
    exit(1)


try:
    with open('alltyrannymentions.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader) 
        row_count = 0
        for row in reader:
            if len(row) != 5:
                print(f"Skipping invalid row in alltyrannymentions.csv: {row}")
                continue
            try:
                mention_id = int(row[0].strip('"'))
                newspaper_name = row[4].strip()  
                cur.execute("SELECT newspaper_id FROM newspapers WHERE title = ?", (newspaper_name,))
                result = cur.fetchone()
                if result:
                    newspaper_id = result[0]
                    cur.execute('''
                        INSERT INTO tyranny_mentions (mention_id, newspaper_id, aka, date, page_number, partof_title)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (mention_id, newspaper_id, row[1], row[2], int(row[3]), row[4]))
                    row_count += 1
                else:
                     print(f"No matching newspaper found for '{newspaper_name}', skipping mention_id {mention_id}")
            except ValueError as e:
                print(f"Error inserting row in alltyrannymentions.csv: {row}, Error: {e}")
                continue
            except sqlite3.Error as e:
                print(f"Database error inserting row in alltyrannymentions.csv: {row}, Error: {e}")
                continue
        print(f"Inserted {row_count} rows into tyranny_mentions table")
except FileNotFoundError:
    print("Error: alltyrannymentions.csv not found")
    conn.close()
    exit(1)
except Exception as e:
    print(f"Unexpected error reading alltyrannymentions.csv: {e}")
    conn.close()
    exit(1)


try:
    conn.commit()
    print("All changes committed to the database")
except sqlite3.Error as e:
    print(f"Error committing changes: {e}")
finally:
    conn.close()
    print("Database connection closed")



