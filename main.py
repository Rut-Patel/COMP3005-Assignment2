import os
from datetime import date
import psycopg


# Opens a connection to the local assignment database.
def _connect() -> psycopg.Connection:
    # Connect to the local assignment database.
    return psycopg.connect(
        dbname=os.getenv("PGDATABASE", "assignment2"),
        user="postgres",
        password= "admin"
    )


# Retrieves and displays all student records.
def getAllStudents() -> list[tuple[int, str, str, str, date | None]]:
    # Get every student from the database.
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query="""
                      SELECT student_id, first_name, last_name, email, enrollment_date
                      FROM students
                      ORDER BY student_id
                      """
            )
            students = cur.fetchall()

    # Show the results in the console.
    print("student_id | first_name | last_name | email | enrollment_date")
    for student in students:
        print(" | ".join("" if value is None else str(value) for value in student))
    return students


# Adds a student record and returns the new student's ID.
def addStudent(
    first_name: str,
    last_name: str,
    email: str,
    enrollment_date: date | None,
) -> int:
    # Add a new student and get the ID created by the database.
    first_name = first_name.strip()
    last_name = last_name.strip()
    email = email.strip()
    if not first_name or not last_name or not email:
        raise ValueError("First name, last name, and email cannot be empty.")

    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                RETURNING student_id
                """,
                (first_name, last_name, email, enrollment_date),
            )
            student_id = cur.fetchone()[0]
    return student_id


# Updates a student's email address using their student ID.
def updateStudentEmail(student_id: int, new_email: str) -> bool:
    # Do not let an empty email replace the current one.
    if not new_email.strip():
        raise ValueError("Email cannot be empty.")

    # Update the email for the student with this ID.
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE students
                SET email = %s
                WHERE student_id = %s
                RETURNING student_id
                """,
                (new_email, student_id),
            )
            updated = cur.fetchone() is not None
    return updated


# Deletes a student record using the student's ID.
def deleteStudent(student_id: int) -> bool:
    # Delete the student with the given ID.
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM students
                WHERE student_id = %s
                RETURNING student_id
                """,
                (student_id,),
            )
            deleted = cur.fetchone() is not None
    return deleted


# Shows the menu and runs the selected student database operation.
def main() -> None:
    # Keep showing the menu until the user chooses to exit.
    while True:
        print(
            "\nStudent Database Menu\n"
            "1. Display all students\n"
            "2. Add a student\n"
            "3. Update a student's email\n"
            "4. Delete a student\n"
            "5. Exit"
        )
        choice = input("Choose an option (1-5): ").strip()

        try:
            # Run the function that matches the user's choice.
            if choice == "1":
                getAllStudents()
            elif choice == "2":
                first_name = input("First name: ").strip()
                last_name = input("Last name: ").strip()
                email = input("Email: ").strip()
                enrollment_text = input(
                    "Enrollment date (YYYY-MM-DD, or leave blank): "
                ).strip()
                enrollment_date = (
                    date.fromisoformat(enrollment_text) if enrollment_text else None
                )
                student_id = addStudent(
                    first_name, last_name, email, enrollment_date
                )
                print(f"Student added with ID {student_id}.")
            elif choice == "3":
                student_id = int(input("Student ID: ").strip())
                new_email = input("New email: ").strip()
                if updateStudentEmail(student_id, new_email):
                    print("Student email updated.")
                else:
                    print(f"No student found with ID {student_id}.")
            elif choice == "4":
                student_id = int(input("Student ID: ").strip())
                if deleteStudent(student_id):
                    print("Student deleted.")
                else:
                    print(f"No student found with ID {student_id}.")
            elif choice == "5":
                print("Goodbye.")
                return
            else:
                print("Please choose a number from 1 to 5.")
        except ValueError as exc:
            print(f"Invalid input: {exc}")
        except psycopg.Error as exc:
            print(f"Database operation failed: {exc}")


if __name__ == "__main__":
    main()
