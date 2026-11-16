# Assignment 3

Assignment 3 application for CRUD to local database.

## Requirements

- Python 3.10 or later
- PostgreSQL
- The `psycopg` Python package

If `psycopg` is not installed, install its binary package:

```bash
python -m pip install "psycopg[binary]"
```

## Set up the database

Create a database named `assignment2` with use postgres and default password if it does not already exist:

```bash
createdb assignment2
```

Create the students table and add the sample records:

```bash
psql -d assignment2 -f schema.sql
```

Run `schema.sql` only once on a new database; it inserts sample records, and
running it again will conflict with the unique email addresses.

The program connects to PostgreSQL on the local machine and uses the
`assignment2` database by default. It uses the PostgreSQL connection settings
configured on your computer. You can set `PGDATABASE` to use a different
database name.

## Run the program

From the project directory, run:

```bash
python main.py
```

## Function definitions

Use the menu to:

1. Display all students.
2. Add a student. Enter the enrollment date as `YYYY-MM-DD`, or leave it blank.
3. Update a student's email using their student ID.
4. Delete a student using their student ID.
5. Exit the program.
