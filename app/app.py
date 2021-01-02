import os
from flask import Flask, flash, redirect, request, send_from_directory, current_app
from flask import render_template
from werkzeug.utils import secure_filename

from app.configs import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, SECRET_KEY
from app.CsvParser import save_answer, get_form_result

ALLOWED_EXTENSIONS = ALLOWED_EXTENSIONS
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/uploads'
app.secret_key = SECRET_KEY


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect('/')
        file = request.files['file']
        if file.filename == '':
            flash('فایلی انتخاب نشده است ', 'danger')
            return redirect('/')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename.replace(' ', '_')  # no space in filenames! because we will call them as command line arguments
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            save_answer(filename)
            flash('فایل با موفقیت تبدیل شد ', 'info')
            return redirect('/')


@app.route('/')
def index():
    answers, students = get_form_result()
    return render_template('index.html', data={'answers': answers, 'students': students})


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
