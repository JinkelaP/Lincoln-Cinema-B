from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash

from globalController import lincolnCinema

bp = Blueprint('login', __name__, )

def is_authenticated():
    return lincolnCinema.loggedin

def getAccountInfo():
    return {
                'name': lincolnCinema.loggedUser.name,
                'auth': lincolnCinema.loggedin,
                'username': lincolnCinema.loggedUser.username
            }

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
            session['accountInfo'] = getAccountInfo()
            return redirect("/")

    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@bp.route('/qc')
def qCustomer():
    loginReturn = lincolnCinema.login('haochenCustomer', 'password', 'Customer')
    flash(f'Welcome back, {loginReturn}!', 'success')
    session['accountInfo'] = getAccountInfo()
    return redirect("/")

@bp.route('/qs')
def qStaff():
    loginReturn = lincolnCinema.login('haochenStaff', 'password', 'Staff')
    flash(f'Welcome back, {loginReturn}!', 'success')
    session['accountInfo'] = getAccountInfo()
    return redirect("/")

@bp.route('/qa')
def qAdmin():
    loginReturn = lincolnCinema.login('haochenAdmin', 'password', 'Admin')
    flash(f'Welcome back, {loginReturn}!', 'success')
    session['accountInfo'] = getAccountInfo()
    return redirect("/")