from flask import flash, render_template, request, redirect, url_for, session, Blueprint

from globalController import lincolnCinema

bp = Blueprint('index', __name__, )
@bp.route("/", methods=['GET'])
def indexPage():
    movieList = []
    for i in lincolnCinema.allMovie:
        if i.status:
            movieInfo = {
                'title': i.title,
                'description': i.description,
                'language': i.language,
                'releaseDate': i.releaseDate,
                'durationMin': i.durationMin
            }
            movieList.append(movieInfo)

    if lincolnCinema.loggedin == None:
        return render_template('index.html',movieList=movieList)
    else:
        user = lincolnCinema.loggedUser
        accountInfo = {
            'name': user.name
        }
        return render_template('index.html', accountInfo=accountInfo, movieList=movieList)