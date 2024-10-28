from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Hardcoded dummy data for now
students = [
    {
        'id': 1,
        'name': 'Elly',
        'levels': [
            {'name': 'Lesson 1', 'letter': 'A', 'completed': True, 'accuracy': 90, 'mistakes': 'Confused D with B'},
            {'name': 'Lesson 2', 'letter': 'C', 'completed': True, 'accuracy': 85, 'mistakes': 'Confused C with G'},
            {'name': 'Lesson 3', 'letter': 'E', 'completed': False, 'accuracy': 0, 'mistakes': ''},
            {'name': 'Lesson 4', 'letter': 'B', 'completed': False, 'accuracy': 0, 'mistakes': ''},
            {'name': 'Lesson 5', 'letter': 'D', 'completed': False, 'accuracy': 0, 'mistakes': ''}
        ]
    },
    {
        'id': 2,
        'name': 'Bob',
        'levels': [
            {'name': 'Lesson 1', 'letter': 'E', 'completed': True, 'accuracy': 75, 'mistakes': 'Confused E with F'},
            {'name': 'Lesson 2', 'letter': 'D', 'completed': True, 'accuracy': 80, 'mistakes': ''},
            {'name': 'Lesson 3', 'letter': 'F', 'completed': False, 'accuracy': 0, 'mistakes': ''},
            {'name': 'Lesson 4', 'letter': 'A', 'completed': False, 'accuracy': 0, 'mistakes': ''},
            {'name': 'Lesson 5', 'letter': 'C', 'completed': False, 'accuracy': 0, 'mistakes': ''}
        ]
    },
    {
        'id': 3,
        'name': 'Yeasin',
        'levels': [
            {'name': 'Lesson 1', 'letter': 'B', 'completed': True, 'accuracy': 95, 'mistakes': 'Confused B with D'},
            {'name': 'Lesson 2', 'letter': 'O', 'completed': True, 'accuracy': 90, 'mistakes': ''},
            {'name': 'Lesson 3', 'letter': 'N', 'completed': True, 'accuracy': 85, 'mistakes': ''},
            {'name': 'Lesson 4', 'letter': 'M', 'completed': True, 'accuracy': 80, 'mistakes': ''},
            {'name': 'Lesson 5', 'letter': 'P', 'completed': True, 'accuracy': 88, 'mistakes': ''}
        ]
    }
]

def compute_progress(levels):
    completed = sum(1 for level in levels if level['completed'])
    total = len(levels)
    percent = int((completed / total) * 100)
    progress_text = f"{completed}/{total} lessons completed"
    return progress_text, percent

@app.route('/')
def dashboard():
    for student in students:
        progress_text, progress_percent = compute_progress(student['levels'])
        student['progress'] = progress_text
        student['progress_percent'] = progress_percent
    return render_template('dashboard.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        new_id = len(students) + 1
        new_name = request.form['name']
        default_levels = [
            {'name': 'Lesson 1', 'letter': 'A', 'completed': False, 'accuracy': 0, 'mistakes': ''},
            {'name': 'Lesson 2', 'letter': 'B', 'completed': False, 'accuracy': 0, 'mistakes': ''},
            {'name': 'Lesson 3', 'letter': 'C', 'completed': False, 'accuracy': 0, 'mistakes': ''},
            {'name': 'Lesson 4', 'letter': 'D', 'completed': False, 'accuracy': 0, 'mistakes': ''},
            {'name': 'Lesson 5', 'letter': 'E', 'completed': False, 'accuracy': 0, 'mistakes': ''}
        ]
        new_student = {'id': new_id, 'name': new_name, 'levels': default_levels}
        students.append(new_student)
    return redirect(url_for('dashboard'))

@app.route('/student/<int:student_id>')
def student_progress(student_id):
    student = next((s for s in students if s['id'] == student_id), None)
    if student is None:
        return redirect(url_for('dashboard'))
    return render_template('student_progress.html', student=student)

@app.route('/remove_student/<int:student_id>', methods=['POST'])
def remove_student(student_id):
    global students
    students = [s for s in students if s['id'] != student_id]
    return redirect(url_for('dashboard'))

@app.route('/skip_to_level/<int:student_id>/<int:level_index>', methods=['POST'])
def skip_to_level(student_id, level_index):
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        for i in range(len(student['levels'])):
            if i <= level_index:
                student['levels'][i]['completed'] = True
            else:
                student['levels'][i]['completed'] = False
    return redirect(url_for('student_progress', student_id=student_id))

if __name__ == '__main__':
    app.run(debug=True)
