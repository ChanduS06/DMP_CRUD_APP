import sys, os
from os import abort
from flask_login import login_required, current_user, login_user, logout_user
from flask import Flask, render_template, request, redirect, url_for
from models import db, EmployeeModel, login, UserModel, UGStudentsModel, PGStudentsModel, FacultyModel

import pandas as pd
import sqlite3

from flask_autodoc.autodoc import Autodoc

app = Flask(__name__)
app.secret_key = 'xyz'

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
auto = Autodoc(app)

db.init_app(app)
login.init_app(app)
login.login_view = 'login'


conn = sqlite3.connect('data.db')
print("Opened database successfully", file=sys.stderr)
cur = conn.cursor()
conn.execute('''SELECT * from UGStudents''')
rows = cur.fetchall()
print(rows, "abcd", file=sys.stderr)
conn.close()


@auto.doc()
@app.before_first_request
def create_table():
    db.create_all()


@auto.doc()
@app.route('/upload_csv')
def index():
    # Set The upload HTML template '\templates\upload_form.html'
    return render_template('upload_form.html')


@auto.doc()
# Get the uploaded files
@app.route("/upload_csv", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
    # save the file
    return redirect('/homepage')


@auto.doc()
@app.route('/homepage')
@login_required
def hpmepage():
    ug_len = UGStudentsModel.query.count()
    pg_len = PGStudentsModel.query.count()
    fac_len = FacultyModel.query.count()
    emp_len = EmployeeModel.query.count()
    data = [ug_len, pg_len, fac_len, emp_len]
    # print(data, file=sys.stderr)
    return render_template('homepage.html', data=data)


@auto.doc()
@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        employee = EmployeeModel(employee_id=employee_id, name=name, age=age, position=position)
        db.session.add(employee)
        db.session.commit()
        return redirect('/data')


@auto.doc()
@app.route('/ugstudentsdata/ugcreate', methods=['GET', 'POST'])
def ugcreate():
    if request.method == 'GET':
        return render_template('ugCreatePage.html')

    if request.method == 'POST':
        student_id = request.form.get('student_id', '')
        primary_name = request.form.get('primary_name', '')
        middle_name = request.form.get('middle_name', '')
        last_name = request.form.get('last_name', '')
        age = request.form.get('age', '')
        contact_num = request.form.get('contact_num', '')
        primary_email = request.form.get('primary_email', '')
        secondary_email = request.form.get('secondary_email', '')
        uni_email = request.form.get('uni_email', '')
        sex = request.form.get('sex', '')
        address = request.form.get('address', '')
        admission_year = request.form.get('admission_year', '')
        highest_qual = request.form.get('highest_qual', '')
        ugstudents = UGStudentsModel(student_id=student_id, primary_name=primary_name, middle_name=middle_name,
                                     last_name=last_name, age=age, contact_num=contact_num, primary_email=primary_email,
                                     secondary_email=secondary_email, uni_email=uni_email, sex=sex, address=address,
                                     admission_year=admission_year, highest_qual=highest_qual)
        db.session.add(ugstudents)
        db.session.commit()
        return redirect('/ugstudentsdata')


@auto.doc()
@app.route('/ugstudentsdata')
def RetrieveUGStudList():
    ugstudents = UGStudentsModel.query.all()
    return render_template('ugStudsDataList.html', ugstudents=ugstudents)


@auto.doc()
@app.route('/ugstudentsdata/<int:id>')
def RetrieveUGStud(id):
    ugstudents = UGStudentsModel.query.filter_by(student_id=id).first()
    if ugstudents:
        return render_template('ugStudentData.html', ugstudents=ugstudents)
    return f"UG Student with id ={id} Doesn't exist"


@auto.doc()
@app.route('/ugstudentsdata/<int:id>/update', methods=['GET', 'POST'])
def updateUGStud(id):
    ugstudents = UGStudentsModel.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        if ugstudents:
            db.session.delete(ugstudents)
            db.session.commit()
            primary_name = request.form.get('primary_name', '')
            middle_name = request.form.get('middle_name', '')
            last_name = request.form.get('last_name', '')
            age = request.form.get('age', '')
            contact_num = request.form.get('contact_num', '')
            primary_email = request.form.get('primary_email', '')
            secondary_email = request.form.get('secondary_email', '')
            uni_email = request.form.get('uni_email', '')
            sex = request.form.get('sex', '')
            address = request.form.get('address', '')
            admission_year = request.form.get('admission_year', '')
            highest_qual = request.form.get('highest_qual', '')
            ugstudents = UGStudentsModel(student_id=id, primary_name=primary_name, middle_name=middle_name,
                                         last_name=last_name, age=age, contact_num=contact_num,
                                         primary_email=primary_email, secondary_email=secondary_email, uni_email=uni_email, sex=sex, address=address,
                                         admission_year=admission_year, highest_qual=highest_qual)
            db.session.add(ugstudents)
            db.session.commit()
            return redirect(f'/ugstudentsdata/{id}')
        return f"UG Student with id = {id} Does not exist"

    return render_template('updateUGData.html', ugstudents=ugstudents)


@auto.doc()
@app.route('/ugstudentsdata/<int:id>/delete', methods=['GET', 'POST'])
def deleteUGStudent(id):
    ugstudent = UGStudentsModel.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        if ugstudent:
            db.session.delete(ugstudent)
            db.session.commit()
            return redirect('/ugstudentsdata')
        abort(404)

    return render_template('delete.html')


@auto.doc()
@app.route('/pgstudentsdata/pgcreate', methods=['GET', 'POST'])
def pgcreate():
    if request.method == 'GET':
        return render_template('pgCreatePage.html')

    if request.method == 'POST':
        student_id = request.form.get('student_id', '')
        primary_name = request.form.get('primary_name', '')
        middle_name = request.form.get('middle_name', '')
        last_name = request.form.get('last_name', '')
        age = request.form.get('age', '')
        contact_num = request.form.get('contact_num', '')
        primary_email = request.form.get('primary_email', '')
        secondary_email = request.form.get('secondary_email', '')
        uni_email = request.form.get('uni_email', '')
        sex = request.form.get('sex', '')
        address = request.form.get('address', '')
        admission_year = request.form.get('admission_year', '')
        highest_qual = request.form.get('highest_qual', '')
        pgstudents = PGStudentsModel(student_id=student_id, primary_name=primary_name, middle_name=middle_name,
                                     last_name=last_name, age=age, contact_num=contact_num, primary_email=primary_email,
                                     secondary_email=secondary_email, uni_email=uni_email, sex=sex, address=address,
                                     admission_year=admission_year, highest_qual=highest_qual)
        db.session.add(pgstudents)
        db.session.commit()
        return redirect('/pgstudentsdata')


@auto.doc()
@app.route('/pgstudentsdata')
def RetrievePGStudList():
    pgstudents = PGStudentsModel.query.all()
    return render_template('pgStudsDataList.html', pgstudents=pgstudents)


@auto.doc()
@app.route('/pgstudentsdata/<int:id>')
def RetrievePGStud(id):
    pgstudents = PGStudentsModel.query.filter_by(student_id=id).first()
    if pgstudents:
        return render_template('pgStudentData.html', pgstudents=pgstudents)
    return f"UG Student with id ={id} Doesn't exist"


@auto.doc()
@app.route('/pgstudentsdata/<int:id>/update', methods=['GET', 'POST'])
def updatePGStud(id):
    pgstudents = PGStudentsModel.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        if pgstudents:
            db.session.delete(pgstudents)
            db.session.commit()
            primary_name = request.form.get('primary_name', '')
            middle_name = request.form.get('middle_name', '')
            last_name = request.form.get('last_name', '')
            age = request.form.get('age', '')
            contact_num = request.form.get('contact_num', '')
            primary_email = request.form.get('primary_email', '')
            secondary_email = request.form.get('secondary_email', '')
            uni_email = request.form.get('uni_email', '')
            sex = request.form.get('sex', '')
            address = request.form.get('address', '')
            admission_year = request.form.get('admission_year', '')
            highest_qual = request.form.get('highest_qual', '')
            pgstudents = PGStudentsModel(student_id=id, primary_name=primary_name, middle_name=middle_name,
                                         last_name=last_name, age=age, contact_num=contact_num,
                                         primary_email=primary_email,
                                         secondary_email=secondary_email, uni_email=uni_email, sex=sex, address=address,
                                         admission_year=admission_year, highest_qual=highest_qual)
            db.session.add(pgstudents)
            db.session.commit()
            return redirect(f'/pgstudentsdata/{id}')
        return f"PG Student with id = {id} Does not exist"

    return render_template('updatePGData.html', pgstudents=pgstudents)


@auto.doc()
@app.route('/pgstudentsdata/<int:id>/delete', methods=['GET', 'POST'])
def deletePGStudent(id):
    pgstudents = PGStudentsModel.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        if pgstudents:
            db.session.delete(pgstudents)
            db.session.commit()
            return redirect('/pgstudentsdata')
        abort(404)

    return render_template('delete.html')


@auto.doc()
@app.route('/facultydata/facultycreate', methods=['GET', 'POST'])
def facultycreate():
    if request.method == 'GET':
        return render_template('facultyCreatePage.html')

    if request.method == 'POST':
        faculty_id = request.form.get('faculty_id', '')
        primary_name = request.form.get('primary_name', '')
        middle_name = request.form.get('middle_name', '')
        last_name = request.form.get('last_name', '')
        age = request.form.get('age', '')
        contact_num = request.form.get('contact_num', '')
        primary_email = request.form.get('primary_email', '')
        secondary_email = request.form.get('secondary_email', '')
        uni_email = request.form.get('uni_email', '')
        sex = request.form.get('sex', '')
        address = request.form.get('address', '')
        joining_year = request.form.get('joining_year', '')
        highest_qual = request.form.get('highest_qual', '')
        faculty = FacultyModel(faculty_id=faculty_id, primary_name=primary_name, middle_name=middle_name,
                               last_name=last_name, age=age, contact_num=contact_num, primary_email=primary_email,
                               secondary_email=secondary_email, uni_email=uni_email, sex=sex, address=address,
                               joining_year=joining_year, highest_qual=highest_qual)
        db.session.add(faculty)
        db.session.commit()
        return redirect('/facultydata')


@auto.doc()
@app.route('/facultydata')
def RetrieveFacultyList():
    faculty = FacultyModel.query.all()
    return render_template('facultyDataList.html', faculty=faculty)


@auto.doc()
@app.route('/facultydata/<int:id>')
def RetrieveFaculty(id):
    faculty = FacultyModel.query.filter_by(faculty_id=id).first()
    if faculty:
        return render_template('facultyData.html', faculty=faculty)
    return f"Faculty with id ={id} Doesn't exist"


@auto.doc()
@app.route('/facultydata/<int:id>/update', methods=['GET', 'POST'])
def updateFaculty(id):
    faculty = FacultyModel.query.filter_by(faculty_id=id).first()
    if request.method == 'POST':
        if faculty:
            db.session.delete(faculty)
            db.session.commit()
            primary_name = request.form.get('primary_name', '')
            middle_name = request.form.get('middle_name', '')
            last_name = request.form.get('last_name', '')
            age = request.form.get('age', '')
            contact_num = request.form.get('contact_num', '')
            primary_email = request.form.get('primary_email', '')
            secondary_email = request.form.get('secondary_email', '')
            uni_email = request.form.get('uni_email', '')
            sex = request.form.get('sex', '')
            address = request.form.get('address', '')
            joining_year = request.form.get('joining_year', '')
            highest_qual = request.form.get('highest_qual', '')
            faculty = FacultyModel(faculty_id=id, primary_name=primary_name, middle_name=middle_name,
                                   last_name=last_name, age=age, contact_num=contact_num,
                                   primary_email=primary_email,
                                   secondary_email=secondary_email, uni_email=uni_email, sex=sex, address=address,
                                   joining_year=joining_year, highest_qual=highest_qual)
            db.session.add(faculty)
            db.session.commit()
            return redirect(f'/facultydata/{id}')
        return f"Faculty with id = {id} Does not exist"

    return render_template('updateFacultyData.html', faculty=faculty)


@auto.doc()
@app.route('/facultydata/<int:id>/delete', methods=['GET', 'POST'])
def deletefaculty(id):
    faculty = FacultyModel.query.filter_by(faculty_id=id).first()
    if request.method == 'POST':
        if faculty:
            db.session.delete(faculty)
            db.session.commit()
            return redirect('/facultydata')
        abort(404)

    return render_template('delete.html')


@auto.doc()
@app.route('/data')
def RetrieveList():
    employees = EmployeeModel.query.all()
    return render_template('datalist.html', employees=employees)


@auto.doc()
@app.route('/data/<int:id>')
def RetrieveEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee=employee)
    return f"Employee with id ={id} Doesn't exist"


@auto.doc()
@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            name = request.form['name']
            age = request.form['age']
            position = request.form['position']
            employee = EmployeeModel(employee_id=id, name=name, age=age, position=position)
            db.session.add(employee)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Employee with id = {id} Does not exist"

    return render_template('update.html', employee=employee)


@auto.doc()
@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html')


@auto.doc()
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/homepage')
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/homepage')

    return render_template('login.html')


@auto.doc()
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/homepage')
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        if UserModel.query.filter_by(email=email).first():
            return ('Email already Present')
        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@auto.doc()
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/homepage')


@auto.doc()
@app.route('/')
def entry():
    return redirect('/login')


@auto.doc()
def parseCSV(filePath):
    # CVS Column Names
    col_names = ['employee_id', 'name', 'age', 'position', 'high_school']

    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, names=col_names, header=None)

    # values from high_school dropped in the columns of the object.
    csvData.drop(columns=['high_school'], inplace=True)

    missing_values = csvData.isnull().sum()
    # print(“missing values are: {}”.format(missing_values))
    under_threshold_removed = csvData.dropna(axis='index', thresh=2, inplace=False)
    under_threshold_rows = csvData[~csvData.index.isin(under_threshold_removed.index)]
    # print(under_threshold_rows)

    # Set a default category for missing genders.
    csvData['gender'].cat.add_categories(new_categories=['Male'], inplace=True)
    csvData.fillna(value={'gender': 'Male'}, inplace=True)
    # print(csvData.info())

    # Loop through the Rows
    for i, row in csvData.iterrows():
        sql = "INSERT INTO table (employee_id, name, age, position) VALUES (%s, %s, %s, %s)"
        value = (row['employee_id'], row['name'], row['age'], row['position'])
        conn.execute(sql, value, if_exists='append')
        conn.commit()
        print(i, row['employee_id'], row['name'], row['age'], row['position'])


# This route generates HTML of documentation
@app.route('/documentation')
def documentation():
    return auto.html()


app.run(host='localhost', port=5000)
