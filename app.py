from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Hardcoded dummy data for now
students = [
    {'id': 1, 'name': 'Elly', 'progress': '3/5 lessons completed'},
    {'id': 2, 'name': 'Yeasin', 'progress': '2/5 lessons completed'},
    {'id': 3, 'name': 'Khan', 'progress': '5/5 lessons completed'}
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
        students.append({'id': new_id, 'name': new_name, 'progress': new_progress})
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)

