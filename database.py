"""
Student Performance Tracker - Database Layer
This module handles all database operations using SQLite.
"""

import sqlite3
import os
from contextlib import contextmanager

DATABASE_NAME = 'student_tracker.db'

@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    Ensures connections are properly closed.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_database():
    """
    Initialize the database with required tables.
    Creates students and grades tables if they don't exist.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Create students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_number TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create grades table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                grade REAL NOT NULL CHECK(grade >= 0 AND grade <= 100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
                UNIQUE(student_id, subject)
            )
        ''')
        
        conn.commit()


def add_student_to_db(name, roll_number):
    """
    Add a new student to the database.
    
    Args:
        name (str): Student's name
        roll_number (str): Unique roll number
        
    Returns:
        tuple: (success: bool, message: str, student_id: int or None)
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO students (name, roll_number) VALUES (?, ?)',
                (name, roll_number)
            )
            student_id = cursor.lastrowid
            return True, "Student added successfully", student_id
    except sqlite3.IntegrityError:
        return False, f"Student with roll number {roll_number} already exists", None
    except Exception as e:
        return False, f"Database error: {str(e)}", None


def get_student_by_roll_number(roll_number):
    """
    Retrieve a student by their roll number.
    
    Args:
        roll_number (str): Student's roll number
        
    Returns:
        dict: Student data or None if not found
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM students WHERE roll_number = ?',
            (roll_number,)
        )
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None


def get_all_students():
    """
    Retrieve all students from the database.
    
    Returns:
        list: List of student dictionaries
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students ORDER BY name')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def add_grade_to_db(student_id, subject, grade):
    """
    Add or update a grade for a student.
    
    Args:
        student_id (int): Student's database ID
        subject (str): Subject name
        grade (float): Grade value (0-100)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Validate grade
        grade_float = float(grade)
        if not (0 <= grade_float <= 100):
            return False, "Grade must be between 0 and 100"
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Use INSERT OR REPLACE to handle both new and updated grades
            cursor.execute('''
                INSERT INTO grades (student_id, subject, grade)
                VALUES (?, ?, ?)
                ON CONFLICT(student_id, subject)
                DO UPDATE SET grade = excluded.grade, created_at = CURRENT_TIMESTAMP
            ''', (student_id, subject, grade_float))
            
            return True, "Grade added successfully"
    except ValueError:
        return False, "Invalid grade value"
    except Exception as e:
        return False, f"Database error: {str(e)}"


def get_student_grades(student_id):
    """
    Get all grades for a specific student.
    
    Args:
        student_id (int): Student's database ID
        
    Returns:
        list: List of grade dictionaries
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT subject, grade FROM grades WHERE student_id = ? ORDER BY subject',
            (student_id,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_student_with_grades(roll_number):
    """
    Get complete student information including all grades.
    
    Args:
        roll_number (str): Student's roll number
        
    Returns:
        dict: Complete student data with grades or None if not found
    """
    student = get_student_by_roll_number(roll_number)
    
    if not student:
        return None
    
    grades = get_student_grades(student['id'])
    
    # Convert grades list to dictionary
    grades_dict = {grade['subject']: grade['grade'] for grade in grades}
    
    # Calculate average
    average = sum(grades_dict.values()) / len(grades_dict) if grades_dict else 0
    
    return {
        'id': student['id'],
        'name': student['name'],
        'roll_number': student['roll_number'],
        'grades': grades_dict,
        'average': round(average, 2)
    }


def get_all_students_with_grades():
    """
    Get all students with their complete grade information.
    
    Returns:
        list: List of student dictionaries with grades
    """
    students = get_all_students()
    result = []
    
    for student in students:
        grades = get_student_grades(student['id'])
        grades_dict = {grade['subject']: grade['grade'] for grade in grades}
        average = sum(grades_dict.values()) / len(grades_dict) if grades_dict else 0
        
        result.append({
            'id': student['id'],
            'name': student['name'],
            'roll_number': student['roll_number'],
            'grades': grades_dict,
            'average': round(average, 2)
        })
    
    return result


def get_subject_topper(subject):
    """
    Find the top-performing student in a specific subject.
    
    Args:
        subject (str): Subject name
        
    Returns:
        dict: Topper information or None if no data
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.name, s.roll_number, g.grade
            FROM students s
            JOIN grades g ON s.id = g.student_id
            WHERE g.subject = ?
            ORDER BY g.grade DESC
            LIMIT 1
        ''', (subject,))
        
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None


def get_class_average(subject):
    """
    Calculate the class average for a specific subject.
    
    Args:
        subject (str): Subject name
        
    Returns:
        float: Class average or None if no data
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT AVG(grade) as average
            FROM grades
            WHERE subject = ?
        ''', (subject,))
        
        row = cursor.fetchone()
        
        if row and row['average'] is not None:
            return round(row['average'], 2)
        return None


def get_all_subjects():
    """
    Get a list of all unique subjects in the database.
    
    Returns:
        list: List of subject names
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT subject FROM grades ORDER BY subject')
        rows = cursor.fetchall()
        return [row['subject'] for row in rows]


def delete_student(roll_number):
    """
    Delete a student and all their grades.
    
    Args:
        roll_number (str): Student's roll number
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM students WHERE roll_number = ?', (roll_number,))
            
            if cursor.rowcount == 0:
                return False, "Student not found"
            
            return True, "Student deleted successfully"
    except Exception as e:
        return False, f"Database error: {str(e)}"


# Initialize database when module is imported
init_database()
