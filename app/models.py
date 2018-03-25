from datetime import datetime,date
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager



class Permission:
	# FOLLOW = 0x01
	WORKER = 0x02
	STUDENT = 0x04
	MANAGER = 0x08
	ADMINISTER = 0x80


class Role(db.Model):
	# ...
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref='role')

	def __repr__(self):
		return '<Role %r>' % self.name


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	userid = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password = db.Column(db.String(128))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))



class Student(db.Model):
	__tablename__ = 'student'
	id = db.Column(db.String(64), db.ForeignKey('users.userid'),primary_key=True)
	name =  db.Column(db.String(64))
	room_no = db.Column(db.CHAR(4))
	veg_nonveg = db.Column(db.Boolean)

class Student_Phone(db.Model):
	__tablename__ = 'student_phone'
	student_id = db.Column(db.String(64), db.ForeignKey('student.id'),primary_key=True)
	phone = db.Column(db.Integer,)

class Menu_Item(db.Model):
	__tablename__ = 'menu_item'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64))
	price = db.Column(db.Integer)

class Student_Preference(db.Model):
	__tablename__ = 'student_preference'
	student_id = db.Column(db.String(64), db.ForeignKey('student.id'), primary_key=True)
	day = db.Column(db.String(64),primary_key=True)
	meal_type = db.Column(db.String(64),primary_key=True)
	item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), primary_key=True)
	quantity = db.Column(db.Integer)

class Complaint(db.Model):
	__tablename__ = 'complaint'
	complaint_no = db.Column(db.Integer,primary_key=True)
	student_id = db.Column(db.String(64), db.ForeignKey('student.id'))
	complain_txt = db.Column(db.Text())

class Attendance(db.Model):
	__tablename__ = 'attendance'
	student_id = db.Column(db.String(64), db.ForeignKey('student.id'), primary_key=True)
	date = db.Column(db.Date, primary_key= True)
	meal_type = db.Column(db.String(64),primary_key=True)
	presence = db.Column(db.Boolean)

class Bill(db.Model):
	__tablename__ = 'bill'
	bill_id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.String(64), db.ForeignKey('student.id'), unique =True)
	month = db.Column(db.String(64))
	year = db.Column(db.Integer)
	amount = db.Column(db.Integer)

class Meal_TT(db.Model):
	__tablename__ = 'meal_timetable'
	day = db.Column(db.String(64),primary_key= True)
	meal_type = db.Column(db.String(64),primary_key= True)
	item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), primary_key=True)

class Change_Requested(db.Model):
	__tablename__ = 'change_req'
	student_id = db.Column(db.String(64), db.ForeignKey('student.id'), primary_key=True)
	date = db.Column(db.Date, primary_key= True)
	day = db.Column(db.String(64))
	meal_type = db.Column(db.String(64),primary_key= True)
	item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), primary_key=True)
	quantity = db.Column(db.Integer)



@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))