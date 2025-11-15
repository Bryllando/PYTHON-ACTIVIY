from sqlite3 import connect, Row
import os

database = 'db/school.db'


def init_db():
    """Initialize the database and create table if it doesn't exist"""
    conn = connect(database)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            idno TEXT PRIMARY KEY,
            lastname TEXT NOT NULL,
            firstname TEXT NOT NULL,
            course TEXT NOT NULL,
            level TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def get_all():
    """Get all student records"""
    conn = connect(database)
    conn.row_factory = Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students ORDER BY lastname, firstname')
    students = cursor.fetchall()
    conn.close()
    return students


def get_record(student_id):
    """Get a specific student record by ID"""
    conn = connect(database)
    conn.row_factory = Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE idno = ?', (student_id,))
    student = cursor.fetchone()
    conn.close()
    return student


def check_duplicate_id(student_id):
    """Check if student ID already exists"""
    conn = connect(database)
    cursor = conn.cursor()
    cursor.execute('SELECT idno FROM students WHERE idno = ?', (student_id,))
    existing_student = cursor.fetchone()
    conn.close()
    return existing_student is not None


def add_record(student_data):
    """Add a new student record"""
    # Check for duplicate ID first
    if check_duplicate_id(student_data['studentId']):
        return False, "Student ID already exists!"

    conn = connect(database)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO students (idno, lastname, firstname, course, level)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            student_data['studentId'],
            student_data['lastName'],
            student_data['firstName'],
            student_data['course'],
            student_data['level']
        ))
        conn.commit()
        success = True
        message = "Student added successfully!"
    except Exception as e:
        print(f"Error adding record: {e}")
        success = False
        message = f"Error adding student: {e}"
    finally:
        conn.close()
    return success, message


def update_record(student_id, student_data):
    """Update an existing student record"""
    conn = connect(database)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE students 
            SET lastname = ?, firstname = ?, course = ?, level = ?
            WHERE idno = ?
        ''', (
            student_data['lastName'],
            student_data['firstName'],
            student_data['course'],
            student_data['level'],
            student_id
        ))
        conn.commit()
        success = True
        message = "Student updated successfully!"
    except Exception as e:
        print(f"Error updating record: {e}")
        success = False
        message = f"Error updating student: {e}"
    finally:
        conn.close()
    return success, message


def delete_record(student_id):
    """Delete a student record"""
    conn = connect(database)
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM students WHERE idno = ?', (student_id,))
        conn.commit()
        success = True
        message = "Student deleted successfully!"
    except Exception as e:
        print(f"Error deleting record: {e}")
        success = False
        message = f"Error deleting student: {e}"
    finally:
        conn.close()
    return success, message


def get_process():
    """Placeholder for GET processing"""
    pass


def post_process():
    """Placeholder for POST processing"""
    pass
