"""
Student Performance Tracker - Flask Web Application
Main application file with routes and web interface.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import database as db
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Change this in production

# Initialize database
db.init_database()


@app.route('/')
def index():
    """Home page with dashboard."""
    students = db.get_all_students_with_grades()
    total_students = len(students)
    
    # Calculate statistics
    total_grades = sum(len(s['grades']) for s in students)
    students_with_grades = [s for s in students if s['grades']]
    overall_average = sum(s['average'] for s in students_with_grades) / len(students_with_grades) if students_with_grades else 0
    
    # Get all subjects
    subjects = db.get_all_subjects()
    
    return render_template('index.html',
                         total_students=total_students,
                         total_grades=total_grades,
                         overall_average=round(overall_average, 2),
                         total_subjects=len(subjects),
                         recent_students=students[:5])


@app.route('/students')
def students_list():
    """Display list of all students."""
    students = db.get_all_students_with_grades()
    return render_template('students_list.html', students=students)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    """Add a new student."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        roll_number = request.form.get('roll_number', '').strip()
        
        if not name:
            flash('Student name is required', 'error')
            return render_template('add_student.html')
        
        if not roll_number:
            flash('Roll number is required', 'error')
            return render_template('add_student.html')
        
        success, message, student_id = db.add_student_to_db(name, roll_number)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('students_list'))
        else:
            flash(message, 'error')
            return render_template('add_student.html')
    
    return render_template('add_student.html')


@app.route('/add_grades/<roll_number>', methods=['GET', 'POST'])
def add_grades(roll_number):
    """Add grades for a student."""
    student = db.get_student_with_grades(roll_number)
    
    if not student:
        flash('Student not found', 'error')
        return redirect(url_for('students_list'))
    
    if request.method == 'POST':
        # Get all form fields that start with 'subject_'
        subjects = []
        grades = []
        
        for key in request.form:
            if key.startswith('subject_') and request.form[key].strip():
                index = key.split('_')[1]
                subject = request.form[key].strip()
                grade = request.form.get(f'grade_{index}', '').strip()
                
                if subject and grade:
                    subjects.append(subject)
                    grades.append(grade)
        
        if not subjects:
            flash('Please add at least one subject and grade', 'error')
            return render_template('add_grades.html', student=student)
        
        # Add grades to database
        errors = []
        success_count = 0
        
        for subject, grade in zip(subjects, grades):
            success, message = db.add_grade_to_db(student['id'], subject, grade)
            if success:
                success_count += 1
            else:
                errors.append(f"{subject}: {message}")
        
        if success_count > 0:
            flash(f'Successfully added {success_count} grade(s)', 'success')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        
        return redirect(url_for('view_student', roll_number=roll_number))
    
    return render_template('add_grades.html', student=student)


@app.route('/view_student/<roll_number>')
def view_student(roll_number):
    """View detailed student information."""
    student = db.get_student_with_grades(roll_number)
    
    if not student:
        flash('Student not found', 'error')
        return redirect(url_for('students_list'))
    
    return render_template('view_student.html', student=student)


@app.route('/subject_topper')
def subject_topper_form():
    """Display form to select subject for topper."""
    subjects = db.get_all_subjects()
    return render_template('subject_topper.html', subjects=subjects, topper=None)


@app.route('/subject_topper/<subject>')
def subject_topper(subject):
    """Display top student in a subject."""
    subjects = db.get_all_subjects()
    topper = db.get_subject_topper(subject)
    
    if not topper:
        flash(f'No grades found for subject: {subject}', 'warning')
    
    return render_template('subject_topper.html', subjects=subjects, topper=topper, selected_subject=subject)


@app.route('/class_average')
def class_average_form():
    """Display form to select subject for class average."""
    subjects = db.get_all_subjects()
    return render_template('class_average.html', subjects=subjects, average=None)


@app.route('/class_average/<subject>')
def class_average(subject):
    """Display class average for a subject."""
    subjects = db.get_all_subjects()
    average = db.get_class_average(subject)
    
    if average is None:
        flash(f'No grades found for subject: {subject}', 'warning')
    
    return render_template('class_average.html', subjects=subjects, average=average, selected_subject=subject)


@app.route('/export')
def export_data():
    """Export all student data to a text file."""
    students = db.get_all_students_with_grades()
    
    # Create export directory if it doesn't exist
    export_dir = 'exports'
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'student_data_{timestamp}.txt'
    filepath = os.path.join(export_dir, filename)
    
    # Write data to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("STUDENT PERFORMANCE TRACKER - DATA EXPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        if not students:
            f.write("No student data available.\n")
        else:
            for student in students:
                f.write(f"Name: {student['name']}\n")
                f.write(f"Roll Number: {student['roll_number']}\n")
                f.write(f"Average Grade: {student['average']}\n")
                f.write("-" * 40 + "\n")
                
                if student['grades']:
                    f.write("Grades:\n")
                    for subject, grade in sorted(student['grades'].items()):
                        f.write(f"  {subject}: {grade}\n")
                else:
                    f.write("No grades recorded.\n")
                
                f.write("\n" + "=" * 80 + "\n\n")
    
    flash(f'Data exported successfully to {filename}', 'success')
    return send_file(filepath, as_attachment=True)


@app.route('/delete_student/<roll_number>', methods=['POST'])
def delete_student(roll_number):
    """Delete a student."""
    success, message = db.delete_student(roll_number)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('students_list'))


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
