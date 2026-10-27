"""Menu-driven Student Result Management System."""

from decimal import Decimal

import mysql.connector

from db import get_connection, initialize_database

SUBJECTS = [
    ("Python", "python"),
    ("DBMS", "dbms"),
    ("Software Engineering", "software_engineering"),
    ("Mathematics", "mathematics"),
    ("Computer Networks", "computer_networks"),
]
FIELDS = [column for _, column in SUBJECTS]
SELECT_COLUMNS = (
    "roll_no, name, semester, python, dbms, software_engineering, "
    "mathematics, computer_networks, total, percentage, grade, result"
)


def calculate_result(marks):
    """Return a result dictionary from a list of five marks (0-100)."""
    if len(marks) != len(SUBJECTS) or any(
        not isinstance(mark, int) or not 0 <= mark <= 100 for mark in marks
    ):
        raise ValueError("Enter exactly five whole-number marks from 0 to 100.")

    total = sum(marks)
    percentage = round(total / (len(SUBJECTS) * 100) * 100, 2)
    grade = (
        "A" if percentage >= 80 else
        "B" if percentage >= 70 else
        "C" if percentage >= 60 else
        "D" if percentage >= 50 else
        "F"
    )
    status = "Pass" if all(mark >= 35 for mark in marks) else "Fail"
    return {"total": total, "percentage": percentage, "grade": grade, "result": status}


def read_required(prompt, field_name):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(f"{field_name} cannot be empty.")


def enter_marks():
    marks = []
    for subject, _ in SUBJECTS:
        while True:
            value = input(f"{subject} marks (0-100): ").strip()
            try:
                mark = int(value)
                if 0 <= mark <= 100:
                    marks.append(mark)
                    break
                print("Marks must be between 0 and 100.")
            except ValueError:
                print("Enter a whole number between 0 and 100.")
    return marks


def record_to_dict(record):
    keys = [
        "roll_no", "name", "semester", *FIELDS, "total", "percentage", "grade", "result"
    ]
    return dict(zip(keys, record))


def print_student(record):
    student = record_to_dict(record)
    print("\n" + "-" * 54)
    print(f"Roll number : {student['roll_no']}")
    print(f"Name        : {student['name']}")
    print(f"Semester    : {student['semester']}")
    for label, field in SUBJECTS:
        print(f"{label:<22}: {student[field]}")
    percentage = student["percentage"]
    if isinstance(percentage, Decimal):
        percentage = f"{percentage:.2f}"
    print(f"Total       : {student['total']} / 500")
    print(f"Percentage  : {percentage}%")
    print(f"Grade       : {student['grade']}")
    print(f"Result      : {student['result']}")
    print("-" * 54)


def add_student():
    roll_no = read_required("Roll number: ", "Roll number")
    name = read_required("Student name: ", "Name")
    semester = read_required("Semester: ", "Semester")
    marks = enter_marks()
    result = calculate_result(marks)
    values = (roll_no, name, semester, *marks, result["total"], result["percentage"], result["grade"], result["result"])
    columns = "roll_no, name, semester, " + ", ".join(FIELDS) + ", total, percentage, grade, result"
    placeholders = ", ".join(["%s"] * len(values))
    with get_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"INSERT INTO students ({columns}) VALUES ({placeholders})", values)
            connection.commit()
        finally:
            cursor.close()
    print("Student result added successfully.")


def view_students():
    with get_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT {SELECT_COLUMNS} FROM students ORDER BY roll_no")
            rows = cursor.fetchall()
        finally:
            cursor.close()
    if not rows:
        print("No student records found.")
        return
    for row in rows:
        print_student(row)


def search_student():
    roll_no = read_required("Roll number to search: ", "Roll number")
    with get_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"SELECT {SELECT_COLUMNS} FROM students WHERE roll_no = %s", (roll_no,)
            )
            row = cursor.fetchone()
        finally:
            cursor.close()
    if row:
        print_student(row)
    else:
        print("Student not found.")


def update_student():
    roll_no = read_required("Roll number to update: ", "Roll number")
    with get_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"SELECT {SELECT_COLUMNS} FROM students WHERE roll_no = %s", (roll_no,)
            )
            existing = cursor.fetchone()
            if not existing:
                print("Student not found.")
                return
            print("Enter the replacement marks:")
            marks = enter_marks()
            result = calculate_result(marks)
            assignments = ", ".join(f"{field} = %s" for field in FIELDS)
            cursor.execute(
                f"UPDATE students SET {assignments}, total = %s, percentage = %s, "
                "grade = %s, result = %s WHERE roll_no = %s",
                (*marks, result["total"], result["percentage"], result["grade"], result["result"], roll_no),
            )
            connection.commit()
        finally:
            cursor.close()
    print("Student marks and result updated successfully.")


def delete_student():
    roll_no = read_required("Roll number to delete: ", "Roll number")
    with get_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM students WHERE roll_no = %s", (roll_no,))
            deleted = cursor.rowcount > 0
            connection.commit()
        finally:
            cursor.close()
    print("Student record deleted." if deleted else "Student not found.")


def main():
    try:
        initialize_database()
    except mysql.connector.Error as error:
        print("Could not connect to MySQL or initialize the database.")
        print(f"Details: {error}")
        print("Check that MySQL is running and your .env settings are correct.")
        return

    actions = {
        "1": ("Add student result", add_student),
        "2": ("View all results", view_students),
        "3": ("Search by roll number", search_student),
        "4": ("Update student marks", update_student),
        "5": ("Delete student record", delete_student),
    }
    while True:
        print("\nSTUDENT RESULT MANAGEMENT SYSTEM")
        for choice, (label, _) in actions.items():
            print(f"{choice}. {label}")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        action = actions.get(choice)
        if action is None:
            print("Choose a valid menu option.")
            continue
        try:
            action[1]()
        except mysql.connector.Error as error:
            print(f"MySQL operation failed: {error}")


if __name__ == "__main__":
    main()
