from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash

from globalController import lincolnCinema

bp = Blueprint('logout', __name__, )

@bp.route('/logout')
def logout():
    #Log out through controller
    logoutReturn = lincolnCinema.logout()
    session.pop('accountInfo', None)
    flash( logoutReturn , 'success'), 
    # Redirect to login page
    return redirect('/')