from datetime import datetime,date
import calendar
from flask import render_template, session, redirect, url_for, flash, request
from flask_login import logout_user, login_required, login_user, current_user
from . import main
from .forms import LoginForm
from .. import db
from ..models import User
import MySQLdb

dba = MySQLdb.connect(host="localhost", user="root",passwd="dundundun", db="MMS")
cur = dba.cursor()


@main.route('/', methods=['GET', 'POST'])
def index():

    return render_template('login.html')


@main.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        print form.userid.data
        user = User.query.filter_by(userid=form.userid.data).first()
        print user
        if user is not None and user.password == form.password.data:
            if user.role_id == 2:
                login_user(user, form.remember_me.data)
                return redirect(url_for('main.manager'))
            if user.role_id == 3:
                login_user(user, form.remember_me.data)
                return redirect(url_for('main.student'))
        flash('Invalid username or password.')
    return render_template('Admin/pages/examples/login.html', form=form)



@main.route('/student')
@login_required
def student():
    # check if logged in

    print current_user.userid
    # logout_user()
    cur.execute("select name from student where id = '" + current_user.userid + "'")
    name = cur.fetchone()[0]
    print name
    return render_template('Admin/student.html', name = name)


@main.route('/student/pref_show', methods=['GET', 'POST'])
@login_required
def view_pref():
    print str(request.form.get('day'))
    cur.execute("select M.name, S.quantity from menu_item as M join student_preference as S on M.id = S.item_id where S.student_id = '" + current_user.userid + "' and S.meal_type = 'breakfast' and S.day = '" + str(request.form.get('day')) +"'" )
    breakfast_list = [i for i in cur.fetchall()]
    cur.execute("select M.name, S.quantity from menu_item as M join student_preference as S on M.id = S.item_id where S.student_id = '" + current_user.userid + "' and S.meal_type = 'lunch'and S.day = '" + str(request.form.get('day')) +"'")
    lunch_list = [i for i in cur.fetchall()]
    cur.execute("select M.name, S.quantity from menu_item as M join student_preference as S on M.id = S.item_id where S.student_id = '" + current_user.userid + "' and S.meal_type = 'snacks'and S.day = '" + str(request.form.get('day')) +"'")
    snacks_list = [i for i in cur.fetchall()]
    cur.execute("select M.name, S.quantity from menu_item as M join student_preference as S on M.id = S.item_id where S.student_id = '" + current_user.userid + "' and S.meal_type = 'dinner'and S.day = '" + str(request.form.get('day')) +"'")
    dinner_list = [i for i in cur.fetchall()]
    cur.execute("select name from student where id = '" + current_user.userid + "'")
    name = cur.fetchone()[0]
    return render_template('Admin/pages/tables/view_pref.html', name = name, breakfast = breakfast_list, lunch = lunch_list, snacks = snacks_list, dinner = dinner_list)

@main.route('/student/give_pref', methods=['GET', 'POST'])
@login_required
def give_pref():
    # if request.method == "POST" and request.form.get(""):
    day = request.form.get('day')
    cur.execute("select menu_item.id, menu_item.name, menu_item.price from menu_item, meal_timetable where meal_timetable.day='" + str(request.form.get('day')) + "' and meal_timetable.meal_type='Breakfast' and meal_timetable.item_id=menu_item.id;")
    breakfast_list = [i for i in cur.fetchall()]
    cur.execute("select menu_item.id, menu_item.name, menu_item.price from menu_item, meal_timetable where meal_timetable.day='" + str(request.form.get('day')) + "' and meal_timetable.meal_type='Lunch' and meal_timetable.item_id=menu_item.id;")
    lunch_list = [i for i in cur.fetchall()]
    cur.execute("select menu_item.id, menu_item.name, menu_item.price from menu_item, meal_timetable where meal_timetable.day='" + str(request.form.get('day')) + "' and meal_timetable.meal_type='Snacks' and meal_timetable.item_id=menu_item.id;")
    snacks_list = [i for i in cur.fetchall()]
    cur.execute("select menu_item.id, menu_item.name, menu_item.price from menu_item, meal_timetable where meal_timetable.day='" + str(request.form.get('day')) + "' and meal_timetable.meal_type='Dinner' and meal_timetable.item_id=menu_item.id;")
    dinner_list = [i for i in cur.fetchall()]
    cur.execute("select name from student where id = '" + current_user.userid + "'")
    name = cur.fetchone()[0]

    if request.method == "POST":
        print request.form.getlist('brf')
        if request.form.get("give_pref"):
            add_br = [[entry[0],entry[1],entry[2],request.form.getlist('brf')[i]] for i,entry in enumerate(breakfast_list)]

            add_lu = [[entry[0],entry[1],entry[2],request.form.getlist('lun')[i]] for i,entry in enumerate(lunch_list)]
            print (add_lu)
            add_sn = [[entry[0],entry[1],entry[2],request.form.getlist('sna')[i]] for i,entry in enumerate(snacks_list)]
            add_di = [[entry[0],entry[1],entry[2],request.form.getlist('din')[i]] for i,entry in enumerate(dinner_list)]
            for i in add_br:
                cur.execute("delete from student_preference where student_id = '"+ (current_user.userid) + "'and day = '" + str(request.form.get('day')) + "' and meal_type =  'Breakfast' and item_id =  "  + str(i[0]) )
                cur.execute("insert into student_preference values('"+ (current_user.userid) + "', '" + str(request.form.get('day')) + "', 'Breakfast', "  + str(i[0]) + ", " + str(i[3]) + ")")
            for i in add_lu:
                cur.execute("delete from student_preference where student_id = '"+ (current_user.userid) + "'and day = '" + str(request.form.get('day')) + "' and meal_type =  'Lunch' and item_id =  "  + str(i[0]) )
                cur.execute("insert into student_preference values('"+ (current_user.userid) + "', '" + str(request.form.get('day')) + "', 'Lunch', "  + str(i[0]) + ", " + str(i[3]) + ")")
            for i in add_sn:
                cur.execute("delete from student_preference where student_id = '"+ (current_user.userid) + "'and day = '" + str(request.form.get('day')) + "' and meal_type =  'Snacks' and item_id =  "  + str(i[0]) )
                cur.execute("insert into student_preference values('"+ (current_user.userid) + "', '" + str(request.form.get('day')) + "', 'Snacks', "  + str(i[0]) + ", " + str(i[3]) + ")")
            for i in add_di:
                cur.execute("delete from student_preference where student_id = '"+ (current_user.userid) + "'and day = '" + str(request.form.get('day')) + "' and meal_type =  'Dinner' and item_id =  "  + str(i[0]) )
                cur.execute("insert into student_preference values('"+ (current_user.userid) + "', '" + str(request.form.get('day')) + "', 'Dinner', "  + str(i[0]) + ", " + str(i[3]) + ")")

            dba.commit()
            return redirect(url_for('main.view_pref'))


    return render_template('Admin/pages/tables/student_pref.html',name = name, breakfast = breakfast_list, lunch = lunch_list, snacks = snacks_list, dinner = dinner_list , weekday = day)



@main.route('/student/req_change', methods = ['GET','POST'])
@login_required
def req_change():
    my_date = request.form.get('date')
    day = ''
    if my_date:
        my_date = datetime.strptime(my_date, '%Y-%m-%d').date()
        print my_date
        day = str(calendar.day_name[my_date.weekday()])
    meal_type = request.form.get('type')
    if not meal_type:
        meal_type = ''
    cur.execute(
        "select menu_item.id, menu_item.name, menu_item.price from menu_item, meal_timetable where meal_timetable.day='" +str(day) + "' and meal_timetable.meal_type='" + str(meal_type) + "' and meal_timetable.item_id=menu_item.id;")
    item_list = [i for i in cur.fetchall()]
    if request.method == "POST":

        if request.form.get('change'):
            add_req = [[entry[0],entry[1],entry[2],request.form.getlist('qty')[i]] for i,entry in enumerate(item_list)]

            for i in add_req:
                cur.execute(
                    "delete from change_req where student_id = '" + (current_user.userid) + "'and date = '" + str(
                        my_date) + "' and meal_type =  '" + meal_type + "' and item_id =  " + str(i[0]))
                cur.execute("insert into change_req values('" + (current_user.userid) + "', '" + str(
                my_date) + "', '" + day + "', '" + meal_type + "', " + str(i[0]) + ", " + str(i[3]) + ")")
            dba.commit()
            return redirect(url_for('main.req_change'))

        if request.form.get('drop'):
            add_req = [[entry[0], entry[1], entry[2], request.form.getlist('qty')[i]] for i, entry in
                       enumerate(item_list)]
            print add_req
            for i in add_req:
                cur.execute(
                    "delete from change_req where student_id = '" + (current_user.userid) + "'and date = '" + str(
                        my_date) + "' and meal_type =  '" + meal_type + "' and item_id =  " + str(i[0]))
                cur.execute("insert into change_req values('" + (current_user.userid) + "', '" + str(
                    my_date) + "', '" + day + "', '" + meal_type + "', " + str(i[0]) + ", " + str(0) + ")")
            dba.commit()
            return redirect(url_for('main.req_change'))


    cur.execute("select name from student where id = '" + current_user.userid + "'")
    name = cur.fetchone()[0]
    return render_template('Admin/pages/tables/request_change.html',name = name, item_list = item_list , day = day, type = meal_type, date = my_date)

@main.route('/manager')
@login_required
def manager():
    # check if logged in

    print current_user.get_id()
    # logout_user()
    return render_template('Admin/manager.html')

@main.route('/manager/add_delete', methods=['GET', 'POST'])
@login_required
def add_delete():
    cur.execute("select * from menu_item")
    item_list = [i for i in cur.fetchall()]

    if request.method == "POST":
        if request.form.get("del_button"):
            to_delete = request.form.getlist('items')
            for id in to_delete:
                cur.execute("delete from menu_item WHERE item_id  = " + id)

        elif request.form.get("add_button"):
            cur.execute("insert into menu_item(item_name, item_price) values('" + request.form.get('item_name') +"' , " + request.form.get('item_price') + ")" )

        dba.commit()
        return redirect(url_for('main.add_delete'))
    # for entry in item_list:
    # print item_list[0][0]
    return render_template('Admin/pages/tables/add_delete.html',item_list = item_list)

@main.route('/manager/set_timetable', methods=['GET', 'POST'])
@login_required
def set_timetable():
    cur.execute("select * from menu_item")
    item_list = [i for i in cur.fetchall()]

    if request.method == "POST":
        to_add = request.form.getlist('items')
        for id in to_add:
            cur.execute("insert into meal_timetable values('"+ request.form.get('day')+"', '" + request.form.get('meal_type') + "',"  + str(id) + ")")
            print request.form.get('meal_type')
        dba.commit()
        return redirect(url_for('main.set_timetable'))
    return render_template('Admin/pages/tables/set_timetable.html',item_list = item_list)



@main.route('/manager/complaint', methods=['GET', 'POST'])
@login_required
def complaint():
    cur.execute("select * from  complaint")
    complaints = [i for i in cur.fetchall()]
    return render_template('Admin/pages/tables/complaint.html',complaints = complaints)



@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))
