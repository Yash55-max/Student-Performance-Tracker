"""
Student Performance Tracker - Core Models
This module contains the Student and StudentTracker classes for managing student data.
"""

class Student:
    """Represents a student with their grades across different subjects."""
    
    def __init__(self, name, roll_number):
        """
        Initialize a Student object.
        
        Args:
            name (str): Student's name
            roll_number (str): Unique roll number
        """
        self.name = name
        self.roll_number = roll_number
        self.grades = {}  # Dictionary to store subject: grade pairs
    
    def add_grade(self, subject, grade):
        """
        Add or update a grade for a specific subject.
        
        Args:
            subject (str): Subject name
            grade (float): Grade value (0-100)
            
        Returns:
            bool: True if grade was added successfully, False otherwise
        """
        if not self._validate_grade(grade):
            return False
        
        self.grades[subject] = grade
        return True
    
    def _validate_grade(self, grade):
        """
        Validate that a grade is within acceptable range.
        
        Args:
            grade (float): Grade to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            grade_float = float(grade)
            return 0 <= grade_float <= 100
        except (ValueError, TypeError):
            return False
    
    def calculate_average(self):
        """
        Calculate the average grade across all subjects.
        
        Returns:
            float: Average grade, or 0 if no grades exist
        """
        if not self.grades:
            return 0
        
        return sum(self.grades.values()) / len(self.grades)
    
    def get_details(self):
        """
        Get formatted student details.
        
        Returns:
            dict: Dictionary containing student information
        """
        return {
            'name': self.name,
            'roll_number': self.roll_number,
            'grades': self.grades,
            'average': round(self.calculate_average(), 2)
        }
    
    def __str__(self):
        """String representation of the student."""
        avg = self.calculate_average()
        return f"Student: {self.name} (Roll No: {self.roll_number}) - Average: {avg:.2f}"


class StudentTracker:
    """Manages a collection of students and their performance data."""
    
    def __init__(self):
        """Initialize the StudentTracker with an empty student dictionary."""
        self.students = {}  # Dictionary with roll_number as key
    
    def add_student(self, name, roll_number):
        """
        Add a new student to the tracker.
        
        Args:
            name (str): Student's name
            roll_number (str): Unique roll number
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Validate inputs
        if not name or not name.strip():
            return False, "Student name cannot be empty"
        
        if not roll_number or not roll_number.strip():
            return False, "Roll number cannot be empty"
        
        # Check if roll number already exists
        if roll_number in self.students:
            return False, f"Student with roll number {roll_number} already exists"
        
        # Create and add student
        student = Student(name.strip(), roll_number.strip())
        self.students[roll_number] = student
        return True, f"Student {name} added successfully"
    
    def get_student(self, roll_number):
        """
        Retrieve a student by roll number.
        
        Args:
            roll_number (str): Student's roll number
            
        Returns:
            Student: Student object if found, None otherwise
        """
        return self.students.get(roll_number)
    
    def add_grades(self, roll_number, grades_dict):
        """
        Add multiple grades for a student.
        
        Args:
            roll_number (str): Student's roll number
            grades_dict (dict): Dictionary of subject: grade pairs
            
        Returns:
            tuple: (success: bool, message: str)
        """
        student = self.get_student(roll_number)
        
        if not student:
            return False, f"Student with roll number {roll_number} not found"
        
        failed_subjects = []
        for subject, grade in grades_dict.items():
            if not student.add_grade(subject, grade):
                failed_subjects.append(subject)
        
        if failed_subjects:
            return False, f"Invalid grades for subjects: {', '.join(failed_subjects)}"
        
        return True, "Grades added successfully"
    
    def view_student_details(self, roll_number):
        """
        Get detailed information about a student.
        
        Args:
            roll_number (str): Student's roll number
            
        Returns:
            dict: Student details or None if not found
        """
        student = self.get_student(roll_number)
        
        if not student:
            return None
        
        return student.get_details()
    
    def calculate_average(self, roll_number):
        """
        Calculate average grade for a specific student.
        
        Args:
            roll_number (str): Student's roll number
            
        Returns:
            float: Average grade or None if student not found
        """
        student = self.get_student(roll_number)
        
        if not student:
            return None
        
        return student.calculate_average()
    
    def get_all_students(self):
        """
        Get all students in the tracker.
        
        Returns:
            list: List of student details dictionaries
        """
        return [student.get_details() for student in self.students.values()]
    
    def get_subject_topper(self, subject):
        """
        Find the top-performing student in a specific subject.
        
        Args:
            subject (str): Subject name
            
        Returns:
            dict: Dictionary with topper details or None if no data
        """
        students_with_subject = []
        
        for student in self.students.values():
            if subject in student.grades:
                students_with_subject.append({
                    'name': student.name,
                    'roll_number': student.roll_number,
                    'grade': student.grades[subject]
                })
        
        if not students_with_subject:
            return None
        
        # Find student with highest grade
        topper = max(students_with_subject, key=lambda x: x['grade'])
        return topper
    
    def get_class_average(self, subject):
        """
        Calculate the class average for a specific subject.
        
        Args:
            subject (str): Subject name
            
        Returns:
            float: Class average or None if no data
        """
        grades = []
        
        for student in self.students.values():
            if subject in student.grades:
                grades.append(student.grades[subject])
        
        if not grades:
            return None
        
        return sum(grades) / len(grades)
    
    def get_all_subjects(self):
        """
        Get a list of all unique subjects across all students.
        
        Returns:
            list: List of subject names
        """
        subjects = set()
        for student in self.students.values():
            subjects.update(student.grades.keys())
        return sorted(list(subjects))
