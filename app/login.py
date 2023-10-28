from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash

from globalController import lincolnCinema

bp = Blueprint('login', __name__, )

def is_authenticated():
    return lincolnCinema.loggedin

@bp.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if lincolnCinema.loggedin:
        return redirect("/")
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        userPassword = request.form['password']
        userType = request.form['userType']
        loginReturn = lincolnCinema.login(username, userPassword, userType)
        if loginReturn == 404:
            return render_template('login.html', msg='Incorrect username or password!', loginUsername=username)
        else:
            flash(f'Welcome back, {loginReturn}!', 'success')
            return redirect("/")

    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

