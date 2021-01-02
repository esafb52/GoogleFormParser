import os
from flask import Flask, flash, redirect, request, send_from_directory, current_app
from flask import render_template
from werkzeug.utils import secure_filename

from app.configs import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, SECRET_KEY
from app.CsvParser import process_and_save_answers, get_exam_form_result

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = SECRET_KEY


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def file_upload():
    if 'file' not in request.files:
        flash('فایلی انتخاب نشده است ', 'danger')
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        flash('فایلی انتخاب نشده است ', 'danger')
        return redirect('/')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename.replace(' ', '_'))
        file.save(file_path)

        # start process answer
        process_and_save_answers(filename)
        flash('فایل با موفقیت تبدیل شد ', 'info')
        return redirect('/')
    else:
        flash('فرمت فایل انتخابی صحیح نمی باشد ', 'info')
        return redirect('/')


@app.route('/')
def index():
    answers, students = get_exam_form_result()
    count = len(students)
    return render_template('index.html', data={'answers': answers, 'students': students, 'count': count})


@app.route('/download', methods=['GET'])
def download():
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    filename = 'answer.txt'
    if os.path.exists(uploads + '/' + filename):
        return send_from_directory(directory=uploads, filename=filename)
    flash('ابتدا پاسخ آزمون را آپلود کنید ', 'danger')
    return redirect("/")


if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=False)
