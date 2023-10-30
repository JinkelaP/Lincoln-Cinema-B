
from flask import flash, render_template, request, redirect, url_for, session, Blueprint
import os
from datetime import date, datetime, timedelta
from decimal import Decimal
from flask import jsonify
from globalController import lincolnCinema


bp = Blueprint('adminDashboard1', __name__, )

def is_authenticated():
    return lincolnCinema.loggedin

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


@bp.route('/allMovies', methods=['GET'])
def allMovies():
    if is_authenticated():
        movieList = getMovies()

        return render_template('allMovies.html', movieList=movieList)
    else:
        return redirect('/')


@bp.route('/addMovies', methods=['POST'])
def addMovies():
    if is_authenticated():
        title = request.form.get('title')
        description = request.form.get('description')
        language = request.form.get('language')
        releaseDate = request.form.get('releaseDate')
        durationMin = request.form.get('durationMin')
        country = request.form.get('country')
        genre = request.form.get('genre')

        addMovieReturn = lincolnCinema.addMovie(title, description, int(durationMin), language, datetime.strptime(releaseDate, '%Y-%m-%d').date(), country, genre)

        flash(addMovieReturn,'success')
        return redirect('/allMovies')
    else:
        return redirect('/')
    

@bp.route('/addScreenings', methods=['POST'])
def addScreenings():
    if is_authenticated():
        dateT = request.form.get('dateT')
        hallName = request.form.get('hallName')
        movieID = request.form.get('movieID')
        for m in lincolnCinema.allMovie:
            if m.movieID == int(movieID):
                addScreeningReturn = lincolnCinema.addScreening(m, datetime.strptime(dateT, '%Y-%m-%dT%H:%M'), hallName)

        flash(addScreeningReturn,'success')
        return redirect('/allMovies')
    else:
        return redirect('/')


@bp.route('/deleteMovies/<int:movieID>')
def deleteMovie(movieID):
    if is_authenticated():
        for m in lincolnCinema.allMovie:
            if m.movieID == movieID:
                removeMovieReturn = lincolnCinema.removeMovie(m)
                flash(removeMovieReturn, 'success')
                return redirect('/allMovies')
            
        flash('Error', 'success')
        return redirect('/allMovies')
    else:
        return redirect('/')
    
@bp.route('/deleteScreenings/<int:screeningID>')
def deleteScreening(screeningID):
    if is_authenticated():
        for m in lincolnCinema.allScreening:
            if m.screeningID == screeningID:
                removeScreeningReturn = lincolnCinema.removeScreening(m)
                flash(removeScreeningReturn, 'success')
                return redirect('/allMovies')

        flash('Error', 'success')
        return redirect('/allMovies')
    else:
        return redirect('/')