from flask import redirect,url_for,jsonify,request,flash
from flask_login import current_user
from . import main
from ..models import Projects,Tasks
from app import db
import ast


@main.route('/add_project',methods=['GET', 'POST'])
def add_project():	
    if request.method=='POST':
        if current_user.is_authenticated:
            proj = Projects(project_name=request.form['name'],user_id=current_user.id)
            db.session.add(proj)
            db.session.commit()
        else:
            proj = Projects(project_name=request.form['name'],user_id='guest')
            db.session.add(proj)
            db.session.commit()  	
    return redirect(url_for('index'))

@main.route('/delete_project/<id>',methods=['GET','POST'])
def delete_project(id):
    delete_id = id
    taskToDelete = Tasks.query.filter_by(project_id=delete_id).delete()
    projToDelete = Projects.query.filter_by(id=delete_id).first()
    db.session.delete(projToDelete)
    db.session.commit()
    return redirect(url_for('index'))

@main.route('/update_project',methods=['GET','POST'])
def update_project():
    update_id = request.form['id']
    project_name = request.form['project_name']
    print(project_name)
    projToUpdate = Projects.query.filter_by(id=update_id).first()
    projToUpdate.project_name = project_name
    db.session.add(projToUpdate)
    db.session.commit()
    return redirect(url_for('index'))

@main.route('/add_task/<id>',methods=['GET','POST'])
def add_task(id):
    if request.method=='POST':
        task = Tasks(task_name=request.form['task_name'],task_status=False,task_priority=request.form['rangeInput'], \
                date=request.form['task_date'],task_position=0,project_id=id)
        db.session.add(task)
        db.session.commit()        
    return redirect(url_for('index'))

@main.route('/delete_task/<id>',methods=['GET','POST'])
def delete_task(id):
    delete_id = id
    print(delete_id)
    taskToDelete = Tasks.query.get(delete_id)
    db.session.delete(taskToDelete)
    db.session.commit()
    return redirect(url_for('index'))

@main.route('/update_task/<id>',methods=['GET','POST'])
def update_task(id):
    old_name = request.form['task_oldname']
    old_date = request.form['task_olddate']
    name = request.form['task_newname']
    date = request.form['task_newdate']
    taskToUpdate = Tasks.query.filter_by(id=id).first()
    taskToUpdate.task_name = name
    taskToUpdate.date = date
    if name=="" and date=="":
        taskToUpdate.date = old_date
        taskToUpdate.task_name = old_name
    elif name=="":
        taskToUpdate.task_name = old_name
        taskToUpdate.task_date = date
    elif date=="":
        taskToUpdate.task_name = name
        taskToUpdate.date = old_date
    else:
        taskToUpdate.task_name = name  
        taskToUpdate.date = date          
    db.session.add(taskToUpdate)
    db.session.commit()
    return redirect(url_for('index'))


@main.route('/task_done/<id>')
def task_done(id):
    taskDone = Tasks.query.get(id)
    taskDone.task_status = True
    db.session.add(taskDone)
    db.session.commit()
    return redirect(url_for('index'))