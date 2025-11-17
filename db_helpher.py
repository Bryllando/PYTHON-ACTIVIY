from sqlite3 import connect, Row
import os

database = '/temp/school.db'


def init_db():
    """Initialize the database and create table if it doesn't exist"""
    conn = connect(database)
    cursor = conn.cursor()

    # Check if table exists and if profile_picture column exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='students'")
    table_exists = cursor.fetchone()

    if table_exists:
        # Check if profile_picture column exists
        cursor.execute("PRAGMA table_info(students)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'profile_picture' not in columns:
            # Add profile_picture column to existing table
            cursor.execute(
                'ALTER TABLE students ADD COLUMN profile_picture TEXT')
            print("Added profile_picture column to existing table")
    else:
        # Create new table with profile_picture column
        cursor.execute('''
            CREATE TABLE students (
                idno TEXT PRIMARY KEY,
                lastname TEXT NOT NULL,
                firstname TEXT NOT NULL,
                course TEXT NOT NULL,
                level TEXT NOT NULL,
                profile_picture TEXT
            )
        ''')

    # Insert sample data if empty
    cursor.execute('SELECT COUNT(*) FROM students')
    if cursor.fetchone()[0] == 0:
        sample_students = [
            ('1000', 'BAGUIO', 'THEODORE JAVE', 'BSIT', '1', None),
            ('1001', 'DASDA', 'BAG', 'BSIT', '1', None),
            ('1002', 'BROCODE', 'HALO', 'BSIT', '1', None),
            ('1003', 'CHARLIE', 'TANGO', 'BSIT', '2', None),
            ('1004', 'NOVEMBER', 'OSCAR', 'BSIT', '1', None),
            ('1005', 'GUY', 'MILLOR', 'BSCS', '4', None)
        ]
        cursor.executemany('''
            INSERT INTO students (idno, lastname, firstname, course, level, profile_picture)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_students)

    conn.commit()
    conn.close()


def get_all():
    """Get all student records"""
    conn = connect(database)
    conn.row_factory = Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students ORDER BY idno')
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
            INSERT INTO students (idno, lastname, firstname, course, level, profile_picture)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            student_data['studentId'],
            student_data['lastName'].upper(),
            student_data['firstName'].upper(),
            student_data['course'],
            student_data['level'],
            student_data.get('profile_picture')
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
        # Check if profile_picture is in student_data
        if 'profile_picture' in student_data:
            cursor.execute('''
                UPDATE students 
                SET lastname = ?, firstname = ?, course = ?, level = ?, profile_picture = ?
                WHERE idno = ?
            ''', (
                student_data['lastName'].upper(),
                student_data['firstName'].upper(),
                student_data['course'],
                student_data['level'],
                student_data['profile_picture'],
                student_id
            ))
        else:
            cursor.execute('''
                UPDATE students 
                SET lastname = ?, firstname = ?, course = ?, level = ?
                WHERE idno = ?
            ''', (
                student_data['lastName'].upper(),
                student_data['firstName'].upper(),
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
