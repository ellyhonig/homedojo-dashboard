from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Hardcoded dummy data with curriculum progress and lesson details
students = [
    {
        'id': 1,
        'name': 'Alice',
        'progress': '3/5 lessons completed',
        'progress_percent': 60,
        'lessons': [
            {'name': 'Lesson 1', 'status': 'Completed', 'accuracy': 90, 'mistakes': 'Minor typos'},
            {'name': 'Lesson 2', 'status': 'Completed', 'accuracy': 85, 'mistakes': 'Punctuation'},
            {'name': 'Lesson 3', 'status': 'Completed', 'accuracy': 75, 'mistakes': 'Grammar, spelling'},
            {'name': 'Lesson 4', 'status': 'Not Started', 'accuracy': 0, 'mistakes': ''},
            {'name': 'Lesson 5', 'status': 'Not Started', 'accuracy': 0, 'mistakes': ''}
        ]
    },
    {
        'id': 2,
        'name': 'Bob',
        'progress': '2/5 lessons completed',
        'progress_percent': 40,
        'lessons': [
            {'name': 'Lesson 1', 'status': 'Completed', 'accuracy': 80, 'mistakes': 'Spelling errors'},
            {'name': 'Lesson 2', 'status': 'Completed', 'accuracy': 70, 'mistakes': 'Sentence structure'},
            {'name': 'Lesson 3', 'status': 'Not Started', 'accuracy': 0, 'mistakes': ''},
            {'name': 'Lesson 4', 'status': 'Not Started', 'accuracy': 0, 'mistakes': ''},
            {'name': 'Lesson 5', 'status': 'Not Started', 'accuracy': 0, 'mistakes': ''}
        ]
    },
    {
        'id': 3,
        'name': 'Charlie',
        'progress': '5/5 lessons completed',
        'progress_percent': 100,
        'lessons': [
            {'name': 'Lesson 1', 'status': 'Completed', 'accuracy': 95, 'mistakes': 'None'},
            {'name': 'Lesson 2', 'status': 'Completed', 'accuracy': 90, 'mistakes': 'None'},
            {'name': 'Lesson 3', 'status': 'Completed', 'accuracy': 85, 'mistakes': 'Punctuation'},
            {'name': 'Lesson 4', 'status': 'Completed', 'accuracy': 80, 'mistakes': 'Sentence structure'},
            {'name': 'Lesson 5', 'status': 'Completed', 'accuracy': 90, 'mistakes': 'None'}
        ]
    }
]

@app.route('/')
def dashboard():
    return render_template('dashboard.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        new_id = len(students) + 1
        new_name = request.form['name']
        new_progress = '0/5 lessons completed'
        new_student = {
            'id': new_id,
            'name': new_name,
            'progress': new_progress,
            'progress_percent': 0,
            'lessons': [
                {'name': 'Lesson 1', 'status': 'Not Started', 'accuracy': 0, 'mistakes': ''},
                {'name': 'Lesson 2', 'status': 'Not Started', 'accuracy': 0, 'mistakes': ''},
                {'name': 'Lesson 3', 'status': 'Not Started', 'accuracy': 0, 'mistakes': ''},
                {'name': 'Lesson 4', 'status': 'Not Started', 'accuracy': 0, 'mistakes': ''},
                {'name': 'Lesson 5', 'status': 'Not Started', 'accuracy': 0, 'mistakes': ''}
            ]
        }
        students.append(new_student)
    return redirect(url_for('dashboard'))

@app.route('/remove_student/<int:student_id>', methods=['POST'])
def remove_student(student_id):
    global students
    students = [s for s in students if s['id'] != student_id]
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
