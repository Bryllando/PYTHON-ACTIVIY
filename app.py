from flask import Flask, render_template, request, redirect, url_for, flash
from db_helpher import init_db, get_all, get_record, add_record, update_record, delete_record

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages

# Initialize database
init_db()


@app.route('/')
def home():
    students = get_all()
    return render_template('students_table.html', students=students)


@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        student_data = {
            'studentId': request.form['studentId'],
            'lastName': request.form['lastName'],
            'firstName': request.form['firstName'],
            'course': request.form['course'],
            'level': request.form['level']
        }

        success = add_record(student_data)
        if success:
            flash('Student added successfully!', 'success')
        else:
            flash('Error adding student!', 'error')

    return redirect(url_for('home'))


@app.route('/edit_student/<student_id>', methods=['POST'])
def edit_student(student_id):
    if request.method == 'POST':
        student_data = {
            'lastName': request.form['lastName'],
            'firstName': request.form['firstName'],
            'course': request.form['course'],
            'level': request.form['level']
        }

        success = update_record(student_id, student_data)
        if success:
            flash('Student updated successfully!', 'success')
        else:
            flash('Error updating student!', 'error')

    return redirect(url_for('home'))


@app.route('/delete_student/<student_id>')
def delete_student(student_id):
    success = delete_record(student_id)
    if success:
        flash('Student deleted successfully!', 'success')
    else:
        flash('Error deleting student!', 'error')

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
