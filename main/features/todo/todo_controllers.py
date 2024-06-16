from datetime import datetime

from flask import render_template, session, redirect, url_for, request
from flask_login import current_user

from main import app
from main.common.decorators import secured_endpoint
from main.features.todo.todo_models import Todo
from main.features.todo.todo_services import TodoServices


@app.route('/')
@app.route('/todo')
@secured_endpoint
def home(user_id):
    title = request.args.get('title')
    description = request.args.get('description')
    is_complete = request.args.get('is_complete')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Convert is_complete to boolean if it exists
    if is_complete is not None and is_complete != '':
        is_complete = is_complete == '1'
    else:
        is_complete = None

    # Convert start_date and end_date to datetime objects if they exist
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')

    todos = TodoServices.todo_list(user_id, title, description, is_complete, start_date, end_date)
    return render_template('todo/home.html', todos=todos)


@app.route('/todo/add', methods=["GET", "POST"])
@secured_endpoint
def add_todo(user_id):
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        date_time = request.form.get('date_time')

        todo = Todo()
        todo.user_id = user_id
        todo.title = title
        todo.description = description
        todo.date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')

        todo_services = TodoServices()
        todo_services.create_todo(todo)
        return redirect(url_for("home"))
    return render_template("todo/add_todo.html")


@app.route('/todo/update/<todo_id>', methods=["GET", "POST"])
@secured_endpoint
def update_todo(user_id, todo_id):
    todo_services = TodoServices()
    todo_get = todo_services.get_todo(todo_id)
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        date_time = request.form.get('date_time')

        todo = Todo()
        todo.id = todo_id
        todo.user_id = user_id
        todo.title = title
        todo.description = description
        todo.date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
        todo.is_complete = todo_get.is_complete
        print(todo.__dict__)
        todo_services.update_todo(todo)
        return redirect(url_for("home"))
    formatted_time = todo_get.date_time.strftime('%Y-%m-%dT%H:%M')
    return render_template("todo/update_todo.html", todo=todo_get, formatted_time=formatted_time)


@app.route('/todo/delete/<todo_id>')
@secured_endpoint
def delete_todo(user_id, todo_id):
    TodoServices.delete_todo(todo_id)
    return redirect(url_for("home"))


@app.route('/todo/check/<todo_id>')
@secured_endpoint
def check_todo(user_id, todo_id):
    TodoServices.update_is_complete(todo_id)
    return redirect(url_for("home"))
