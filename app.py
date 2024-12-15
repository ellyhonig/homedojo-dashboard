# app.py

from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore
import os
import logging

app = Flask(__name__)

# Configure Logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG for detailed logs
logger = logging.getLogger(__name__)

# Initialize Firebase
firebase_key_path = 'homedojo-dashboard-firebase-adminsdk-gxb7g-a46a4cb39b.json'

if not os.path.exists(firebase_key_path):
    logger.error(f"Firebase admin SDK JSON file '{firebase_key_path}' not found.")
    raise FileNotFoundError(f"Firebase admin SDK JSON file '{firebase_key_path}' not found.")

cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Reference to the 'students' collection
students_ref = db.collection('students')

def compute_progress(levels):
    completed = sum(1 for level in levels if level.get('completed', False))
    total = len(levels)
    percent = int((completed / total) * 100) if total > 0 else 0
    progress_text = f"{completed}/{total} lessons completed"
    return progress_text, percent

@app.route('/')
def dashboard():
    students = []
    try:
        logger.debug("Fetching students from Firestore...")
        docs = students_ref.stream()
        for doc in docs:
            student = doc.to_dict()
            student['id'] = doc.id  # Use Firestore document ID
            # Normalize field names for template consistency
            student['name'] = student.get('Name', 'Unknown')
            student['levels'] = student.get('Levels', [])
            progress_text, progress_percent = compute_progress(student['levels'])
            student['progress'] = progress_text
            student['progress_percent'] = progress_percent
            students.append(student)
            logger.debug(f"Fetched student: {student['name']} with ID: {student['id']}")
    except Exception as e:
        logger.error(f"Error fetching students: {e}")
    return render_template('dashboard.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        new_name = request.form.get('name', '').strip()
        if not new_name:
            logger.warning("Attempted to add a student with an empty name.")
            return redirect(url_for('dashboard'))
        
        default_levels = [
            {'level_name': 'Lesson 1', 'new_letter': 'A', 'completed': False, 'accuracy': 0, 'mistakes': []},
            {'level_name': 'Lesson 2', 'new_letter': 'B', 'completed': False, 'accuracy': 0, 'mistakes': []},
            {'level_name': 'Lesson 3', 'new_letter': 'C', 'completed': False, 'accuracy': 0, 'mistakes': []},
            {'level_name': 'Lesson 4', 'new_letter': 'D', 'completed': False, 'accuracy': 0, 'mistakes': []},
            {'level_name': 'Lesson 5', 'new_letter': 'E', 'completed': False, 'accuracy': 0, 'mistakes': []}
        ]
        new_student = {
            'Name': new_name,
            'Levels': default_levels
        }
        try:
            students_ref.add(new_student)
            logger.info(f"Added new student: {new_name}")
        except Exception as e:
            logger.error(f"Error adding student: {e}")
    return redirect(url_for('dashboard'))

@app.route('/student/<student_id>')
def student_progress(student_id):
    try:
        logger.debug(f"Fetching student with ID: {student_id}")
        student_doc = students_ref.document(student_id).get()
        if not student_doc.exists:
            logger.warning(f"Student with ID {student_id} does not exist.")
            return redirect(url_for('dashboard'))
        student = student_doc.to_dict()
        student['id'] = student_doc.id
        # Normalize field names for template consistency
        student['name'] = student.get('Name', 'Unknown')
        student['levels'] = student.get('Levels', [])
        logger.debug(f"Fetched student progress for: {student['name']}")
        return render_template('student_progress.html', student=student)
    except Exception as e:
        logger.error(f"Error fetching student: {e}")
        return redirect(url_for('dashboard'))

@app.route('/remove_student/<student_id>', methods=['POST'])
def remove_student(student_id):
    try:
        students_ref.document(student_id).delete()
        logger.info(f"Removed student with ID: {student_id}")
    except Exception as e:
        logger.error(f"Error removing student: {e}")
    return redirect(url_for('dashboard'))

@app.route('/skip_to_level/<student_id>/<int:level_index>', methods=['POST'])
def skip_to_level(student_id, level_index):
    try:
        logger.debug(f"Updating progress for student ID {student_id} to level index {level_index}")
        student_doc = students_ref.document(student_id)
        student = student_doc.get().to_dict()
        if not student:
            logger.warning(f"Student with ID {student_id} not found.")
            return redirect(url_for('dashboard'))
        levels = student.get('Levels', [])
        for i in range(len(levels)):
            if i <= level_index:
                levels[i]['completed'] = True
                # Optionally, set accuracy for skipped levels if it's zero
                if levels[i].get('accuracy', 0) == 0:
                    levels[i]['accuracy'] = 100  # Assuming full accuracy when skipped
            else:
                levels[i]['completed'] = False
                levels[i]['accuracy'] = 0
        student_doc.update({'Levels': levels})
        logger.info(f"Updated progress for student ID {student_id} to level index {level_index}")
    except Exception as e:
        logger.error(f"Error updating student progress: {e}")
    return redirect(url_for('student_progress', student_id=student_id))

if __name__ == '__main__':
    app.run(debug=True)
