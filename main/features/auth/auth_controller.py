import json

from flask import request, redirect, url_for, render_template, session
from flask_login import login_user, logout_user

from main import app, client, settings
from main.features.auth.auth_models import User
from main.features.auth.auth_services import AuthServices
import requests


@app.route("/auth")
def auth():
    return render_template('auth/auth.html')


@app.route("/auth/google")
def google():
    auth_s = AuthServices()
    # Find out what URL to hit for Google login
    google_provider_cfg = auth_s.get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route('/auth/google/callback')
def google_callback():
    auth_s = AuthServices()
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = auth_s.get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(settings.GOOGLE_CLIENT_ID, settings.GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    # Create a user in your db with the information provided
    # by Google
    user = User()
    user.id = unique_id
    user.full_name = users_name
    print(picture)

    # Doesn't exist? Add it to the database.
    if not auth_s.get(unique_id):
        auth_s.create_user(user)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("home"))


@app.route("/auth/register", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User()
        user.full_name = request.form['fullName'],
        user.email = request.form["email"],
        user.password = request.form["password"]

        user_dao = AuthServices()
        user_dao.create_user(user)

        return redirect(url_for("user_login"))

    return render_template("auth/register.html")


@app.route('/auth/login', methods=['GET', 'POST'])
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

        return redirect(url_for("home"))
    if session.get('access_token', None) or session.get('access_token', None):
        return redirect(url_for("home"))
    return render_template("auth/login.html")


@app.route('/logout')
def user_logout():
    session.clear()
    logout_user()
    return redirect(url_for('auth'))
