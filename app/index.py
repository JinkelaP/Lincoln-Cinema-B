from flask import flash, render_template, request, redirect, url_for, session, Blueprint

from globalController import lincolnCinema

bp = Blueprint('index', __name__, )


def getAccountInfo():
    return {
                'name': lincolnCinema.loggedUser.name,
                'auth': lincolnCinema.loggedin,
                'username': lincolnCinema.loggedUser.username
            }

def getMovies():
    movieList = []
    for i in lincolnCinema.allMovie:
        movieInfo = {
            'title': i.title,
            'description': i.description,
            'language': i.language,
            'releaseDate': i.releaseDate,
            'durationMin': i.durationMin,
            'country': i.country,
            'genre':i.genre,
            'id': i.movieID,
            'status':i.status,
            'screeningList': i.screeningList
        }
        if i.screeningList:
            sList = []
            for s in i.screeningList:
                screeningInfo = {
                    'screeningID': s.screeningID,
                    'screeningDate': s.screeningDate,
                    'startTime': s.startTime,
                    'endTime': s.endTime,
                    'cinemaHall': s.cinemaHall.name,
                    'status': s.status,
                    'id': s.screeningID,
                    'seats': s.seats
                }
                if s.seats:
                    hsList = []
                    for a in s.seats:
                        theSeat = {
                            'col': a.col,
                            'row': a.row,
                            'seatPlace': a.seatPlace,
                            'isReserved': a.isReserved,
                            'seatPrice': a.seatPrice
                        }
                        hsList.append(theSeat)
                    screeningInfo['seats'] = hsList
                sList.append(screeningInfo)
            movieInfo['screeningList'] = sList
        movieList.append(movieInfo)
    return movieList


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
        return render_template('index.html',movieList=getMovies())

    else:
        return redirect('/')
    
@bp.route("/search", methods=['GET'])
def movieSearch():
    pass