from sqlite3 import connect, Row
import os

# Improved database path handling for Vercel


def get_database_path():
    if 'VERCEL' in os.environ:
        return '/tmp/school.db'
    else:
        return 'school.db'


database = get_database_path()


def init_db():
    """Initialize the database and create table if it doesn't exist"""
    try:
        conn = connect(database)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                idno TEXT PRIMARY KEY,
                lastname TEXT NOT NULL,
                firstname TEXT NOT NULL,
                course TEXT NOT NULL,
                level TEXT NOT NULL,
                profile_picture TEXT
            )
        ''')

        # Check if table has data
        cursor.execute('SELECT COUNT(*) FROM students')
        count = cursor.fetchone()[0]

        if count == 0:
            sample_students = [
                ('1000', 'BAGUIO', 'THEODORE JAVE', 'BSIT', '1', None),
                ('1001', 'DASDA', 'BAG', 'BSIT', '1', None),
                ('1002', 'BROCODE', 'HALO', 'BSIT', '1', None),
                ('1003', 'CHARLIE', 'TANGO', 'BSIT', '2', None),
                ('1004', 'NOVEMBER', 'OSCAR', 'BSIT', '1', None),
                ('1005', 'GUY', 'MILLOR', 'BSCS', '4', None)
            ]
            cursor.executemany('''
                INSERT OR IGNORE INTO students (idno, lastname, firstname, course, level, profile_picture)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', sample_students)

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False

# Rest of your functions remain the same...


def get_all():
    """Get all student records"""
    try:
        conn = connect(database)
        conn.row_factory = Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students ORDER BY idno')
        students = cursor.fetchall()
        conn.close()
        return students
    except Exception as e:
        print(f"Error getting all records: {e}")
        return []


def get_record(student_id):
    """Get a specific student record by ID"""
    try:
        conn = connect(database)
        conn.row_factory = Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE idno = ?', (student_id,))
        student = cursor.fetchone()
        conn.close()
        return student
    except Exception as e:
        print(f"Error getting record: {e}")
        return None


def check_duplicate_id(student_id):
    """Check if student ID already exists"""
    try:
        conn = connect(database)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT idno FROM students WHERE idno = ?', (student_id,))
        existing_student = cursor.fetchone()
        conn.close()
        return existing_student is not None
    except Exception as e:
        print(f"Error checking duplicate: {e}")
        return False


def add_record(student_data):
    """Add a new student record"""
    try:
        # Check for duplicate ID first
        if check_duplicate_id(student_data['studentId']):
            return False, "Student ID already exists!"

        conn = connect(database)
        cursor = conn.cursor()
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
        conn.close()
        return True, "Student added successfully!"
    except Exception as e:
        print(f"Error adding record: {e}")
        return False, f"Error adding student: {e}"


def update_record(student_id, student_data):
    """Update an existing student record"""
    try:
        conn = connect(database)
        cursor = conn.cursor()

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
        conn.close()
        return True, "Student updated successfully!"
    except Exception as e:
        print(f"Error updating record: {e}")
        return False, f"Error updating student: {e}"


def delete_record(student_id):
    """Delete a student record"""
    try:
        conn = connect(database)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE idno = ?', (student_id,))
        conn.commit()
        conn.close()
        return True, "Student deleted successfully!"
    except Exception as e:
        print(f"Error deleting record: {e}")
        return False, f"Error deleting student: {e}"
