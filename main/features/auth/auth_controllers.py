from flask import request, redirect, url_for, render_template, session

from main import app
from main.common.decorators import secured_endpoint
from main.features.auth.auth_models import User
from main.features.auth.auth_services import AuthServices


@app.route("/register", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User()
        user.full_name = request.form['fullName'],
        user.email = request.form["email"],
        user.password = request.form["password"]

        user_dao = AuthServices()
        user_dao.create_user(user)

        return redirect(url_for("user_login"))
    if session.get('access_token', None):
        return redirect(url_for("todo"))
    return render_template("auth/register.html")


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == "POST":
        user_vo = User()
        user_vo.email = request.form["email"],
        user_vo.password = request.form["password"]

        user_dao = AuthServices()
        user_data = user_dao.get_user(user_vo)

        if user_data is None:
            return redirect(url_for("user_login"))

        access_token = user_dao.encode_auth_token(user_data.id)

        # Store tokens in session
        session['access_token'] = access_token
        session['user_id'] = user_data.id

        return redirect(url_for("home"))
    if session.get('access_token', None):
        return redirect(url_for("home"))
    return render_template("auth/login.html")


@app.route('/logout')
def user_logout():
    session.clear()
    return redirect(url_for('user_login'))


@app.route('/user')
@secured_endpoint
def user(user_id):
    user = AuthServices.load_user(user_id)
    return render_template('auth/user.html', user=user)
