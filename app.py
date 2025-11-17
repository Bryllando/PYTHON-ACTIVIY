from flask import Flask, render_template, request, redirect, url_for, flash
from db_helpher import init_db, get_all, get_record, add_record, update_record, delete_record
import base64
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key_here')

# Initialize database on startup
init_db()


@app.route('/')
def home():
    students = get_all()
    return render_template('students_table.html', students=students)


@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        profile_picture = None
        if 'profile_picture' in request.files and request.files['profile_picture'].filename != '':
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                profile_picture = base64.b64encode(file.read()).decode('utf-8')

        student_data = {
            'studentId': request.form['studentId'],
            'lastName': request.form['lastName'],
            'firstName': request.form['firstName'],
            'course': request.form['course'],
            'level': request.form['level'],
            'profile_picture': profile_picture
        }

        success, message = add_record(student_data)
        if success:
            flash('Student added successfully!', 'success')
        else:
            flash(message, 'error')

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

        if 'profile_picture' in request.files and request.files['profile_picture'].filename != '':
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                student_data['profile_picture'] = base64.b64encode(
                    file.read()).decode('utf-8')

        success, message = update_record(student_id, student_data)
        if success:
            flash('Student updated successfully!', 'success')
        else:
            flash(message, 'error')

    return redirect(url_for('home'))


@app.route('/delete_student/<student_id>')
def delete_student(student_id):
    success, message = delete_record(student_id)
    if success:
        flash('Student deleted successfully!', 'success')
    else:
        flash(message, 'error')

    return redirect(url_for('home'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


# Vercel needs this
if __name__ == "__main__":
    app.run(debug=True)
