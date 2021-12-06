from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,LoginManager

login = LoginManager()
db = SQLAlchemy()


class UGStudentsModel(db.Model):
    __tablename__ = "UGStudents"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer(), unique=True)
    primary_name = db.Column(db.String())
    middle_name = db.Column(db.String())
    last_name = db.Column(db.String())
    contact_num = db.Column(db.String())
    primary_email = db.Column(db.String())
    secondary_email = db.Column(db.String())
    uni_email = db.Column(db.String())
    age = db.Column(db.Integer())
    sex = db.Column(db.String())
    address = db.Column(db.String(80))
    admission_year = db.Column(db.Integer())
    highest_qual = db.Column(db.String())

    def __init__(self, student_id, primary_name, middle_name, last_name, age, contact_num,
                 primary_email, secondary_email, uni_email, sex, address, admission_year, highest_qual):
        self.student_id = student_id
        self.primary_name = primary_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.age = age
        self.contact_num = contact_num
        self.primary_email = primary_email
        self.secondary_email = secondary_email
        self.uni_email = uni_email
        self.sex = sex
        self.address = address
        self.admission_year = admission_year
        self.highest_qual = highest_qual

    def __repr__(self):
        return f"{self.last_name}:{self.student_id}"


class PGStudentsModel(db.Model):
    __tablename__ = "PGStudents"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer(), unique=True)
    primary_name = db.Column(db.String())
    middle_name = db.Column(db.String())
    last_name = db.Column(db.String())
    contact_num = db.Column(db.String())
    primary_email = db.Column(db.String())
    secondary_email = db.Column(db.String())
    uni_email = db.Column(db.String())
    age = db.Column(db.Integer())
    sex = db.Column(db.String())
    address = db.Column(db.String(80))
    admission_year = db.Column(db.Integer())
    highest_qual = db.Column(db.String())

    def __init__(self, student_id, primary_name, middle_name, last_name, age, contact_num,
                 primary_email, secondary_email, uni_email, sex, address, admission_year, highest_qual):
        self.student_id = student_id
        self.primary_name = primary_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.age = age
        self.contact_num = contact_num
        self.primary_email = primary_email
        self.secondary_email = secondary_email
        self.uni_email = uni_email
        self.sex = sex
        self.address = address
        self.admission_year = admission_year
        self.highest_qual = highest_qual

    def __repr__(self):
        return f"{self.last_name}:{self.student_id}"


class MyDateTime(db.TypeDecorator):
    impl = db.DateTime

    def process_bind_param(self, value, dialect):
        if type(value) is str:
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        return value


class FacultyModel(db.Model):
    __tablename__ = "FacultyDataa"

    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer(), unique=True)
    primary_name = db.Column(db.String())
    middle_name = db.Column(db.String())
    last_name = db.Column(db.String())
    contact_num = db.Column(db.String())
    primary_email = db.Column(db.String())
    secondary_email = db.Column(db.String())
    uni_email = db.Column(db.String())
    age = db.Column(db.Integer())
    sex = db.Column(db.String())
    address = db.Column(db.String(80))
    joining_year = db.Column(db.String())
    highest_qual = db.Column(db.String())

    def __init__(self, faculty_id, primary_name, middle_name, last_name, age, contact_num,
                 primary_email, secondary_email, uni_email, sex, address, joining_year, highest_qual):
        self.faculty_id = faculty_id
        self.primary_name = primary_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.age = age
        self.contact_num = contact_num
        self.primary_email = primary_email
        self.secondary_email = secondary_email
        self.uni_email = uni_email
        self.sex = sex
        self.address = address
        self.joining_year = joining_year
        self.highest_qual = highest_qual

    def __repr__(self):
        return f"{self.last_name}:{self.faculty_id}"


class EmployeeModel(db.Model):
    __tablename__ = "table"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer(), unique=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    position = db.Column(db.String(80))

    def __init__(self, employee_id, name, age, position):
        self.employee_id = employee_id
        self.name = name
        self.age = age
        self.position = position

    def __repr__(self):
        return f"{self.name}:{self.employee_id}"


class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))
