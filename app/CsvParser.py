import csv
import os
from shutil import copyfile

UPLOAD_BASE_DIR = 'uploads/'


def clean_extra_char(input_text):
    return str(input_text) \
        .replace('u200e', ' ') \
        .replace('u200c', ' ') \
        .replace('\\', '') \
        .replace('\n', ' ')


def process_and_save_answers(file_name):
    students = []
    lst_res = []
    new_student_mode = False
    counter = 0

    input_file = UPLOAD_BASE_DIR + file_name
    last_result_from_input_file = UPLOAD_BASE_DIR + 'last_result.csv'
    copyfile(input_file, last_result_from_input_file)
    out_path = UPLOAD_BASE_DIR + 'answer.txt'
    out_file = open(out_path, mode='w', encoding='utf-8')
    if not os.path.exists(input_file):
        return []
    with open(input_file, encoding='utf-8') as csv_file:
        answers = csv.reader(csv_file, delimiter=',', quotechar='"')
        for answer in answers:
            for item in answer:
                result = clean_extra_char(item)
                if 'گرینویچ' in result:
                    counter = 0
                    out_file.write('.' * 50)
                    new_student_mode = True
                    continue
                if new_student_mode:
                    students.append(item)
                    lst_res.append('دانش آموز جدید' + item)
                    new_student_mode = False
                if result:
                    counter += 1
                    final_answer = ' پاسخ سوال ' + str(counter) + ' : ' + result
                    out_file.write(final_answer + '\n')
                    lst_res.append(final_answer)
                    # print(final_answer)
        out_file.write('\n\n' + 'اسامی شرکت کنندگان آزمون' + '\n')
        counter = 0
        for name in students:
            counter += 1
            out_file.write(str(counter) + ' : ' + name + '\n')
        out_file.close()


def get_exam_form_result():
    students = []
    lst_res = []
    new_student_mode = False
    counter = 0
    input_file = UPLOAD_BASE_DIR + 'last_result.csv'
    if not os.path.exists(input_file):
        return [], []
    with open(input_file, encoding='utf-8') as csv_file:
        answers = csv.reader(csv_file, delimiter=',', quotechar='"')
        for answer in answers:
            for item in answer:
                result = clean_extra_char(item)
                if 'گرینویچ' in result:
                    counter = 0
                    new_student_mode = True
                    continue
                if new_student_mode:
                    lst_res.append('@@@')
                    students.append(item + " | ")
                    new_student_mode = False
                if result:
                    counter += 1
                    final_answer = ' پاسخ سوال ' + str(counter) + ' : ' + result
                    lst_res.append(final_answer)
    return lst_res, students
