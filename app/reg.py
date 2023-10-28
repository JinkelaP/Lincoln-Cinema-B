from flask import flash, render_template, request, redirect, url_for, session, Blueprint
from globalController import lincolnCinema
import re

bp = Blueprint('reg', __name__)

@bp.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('userPassword')
        name = request.form.get('firstName')
        phoneNumber = request.form.get('phoneNumber')
        email = request.form.get('userEmail')
        address = request.form.get('userAddress')

        regReturn = lincolnCinema.register(name, address, email, phoneNumber, username, password)

        if regReturn == 'Conflict':
            flash('Registration fail. Username already existed!', 'success')
            return render_template('register.html')
        else:
            flash('Registration succeeded! You have been logged in!', 'success')
            return redirect(url_for('/'))

    return render_template('register.html')