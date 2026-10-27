# Student Result Management System

A menu-driven Python and MySQL project based on the supplied case study. It demonstrates lists, dictionaries, functions, input validation, parameterized SQL, and CRUD operations.

## Features

- Add, view, search, update, and delete student results.
- Store marks for Python, DBMS, Software Engineering, Mathematics, and Computer Networks.
- Calculate total, percentage, grade, and pass/fail result automatically.
- Create the configured database and `students` table on first launch.

## Requirements

- Python 3.9 or newer
- MySQL Server running locally or remotely

## Setup

1. Open a terminal in this project folder.
2. Install the Python packages: `python -m pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and enter your MySQL host, port, username, password, and database name. Keep `.env` private; it is ignored by Git.
4. Ensure the configured MySQL user can create a database and tables. Alternatively, create the database and table using `schema.sql`, then grant the user access.
5. Start the program with `python main.py`.

The application creates the database and table if they do not exist. The sample database name is `student_result_db`.

## Sample grading rules

The report leaves the exact thresholds configurable. This project uses these example rules in `calculate_result()`:

- Pass when every subject mark is at least 35; otherwise the result is Fail.
- Grade A: percentage >= 80; B: >= 70; C: >= 60; D: >= 50; F: below 50.

Change the thresholds in `main.py` to match your institution's official rules. A student's pass/fail status is determined separately from the percentage grade.

## Database fields

`students` stores `roll_no` (primary key), name, semester, five subject marks, total, percentage, grade, and result. Marks are restricted to the 0-100 range in the application and database schema.

## Project files

- `main.py`: menu, validation, calculations, and student operations.
- `db.py`: MySQL connection settings and automatic database/table setup.
- `schema.sql`: equivalent schema for manual setup in MySQL Workbench.
- `.env.example`: connection settings template.
