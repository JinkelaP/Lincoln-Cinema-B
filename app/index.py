from flask import flash, render_template, request, redirect, url_for, session, Blueprint

from globalController import lincolnCinema

bp = Blueprint('index', __name__, )


def getAccountInfo():
    return {
                'name': lincolnCinema.loggedUser.name,
                'auth': lincolnCinema.loggedin,
                'username': lincolnCinema.loggedUser.username
            }


@bp.route('/')
def realIndex():
    readFileReturn = lincolnCinema.readFileStatus
    if readFileReturn == True:
        # flash('You have read the files.','success')
        return redirect("/index")
    else:
        session.pop('accountInfo', None)
        return render_template('firstOpen.html')



@bp.route('/readFile')
def readFile():
    readFileReturn = lincolnCinema.readFile()

    if readFileReturn['status'] == 'Done':
        flash('Read file successful. Welcome!','success')
        return redirect("/index")
    elif readFileReturn['status'] == 'Has read':
        flash('You have read the files.','success')
        return redirect("/index")

    else:
        flash(f'Read files ERROR,{readFileReturn["status"]}', 'success')
        return redirect("/")



@bp.route("/index", methods=['GET'])
def indexPage():
    if lincolnCinema.readFileStatus == True:
        movieList = []
        for i in lincolnCinema.allMovie:
            if i.status:
                movieInfo = {
                    'title': i.title,
                    'description': i.description,
                    'language': i.language,
                    'releaseDate': i.releaseDate,
                    'durationMin': i.durationMin,
                    'country': i.country,
                    'genre':i.genre,
                    'id': i.movieID
                }
                movieList.append(movieInfo)

        if lincolnCinema.loggedin == None:
            return render_template('index.html',movieList=movieList)
        else:
            accountInfo = {
                'name': lincolnCinema.loggedUser.name,
                'auth': lincolnCinema.loggedin
            }
            return render_template('index.html', accountInfo=accountInfo, movieList=movieList)
    else:
        return redirect('/')
    
@bp.route("/search", methods=['GET'])
def movieSearch():
    pass