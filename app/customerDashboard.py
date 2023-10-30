
from flask import flash, render_template, request, redirect, url_for, session, Blueprint, jsonify
import json
import os
from decimal import Decimal
from datetime import datetime, timezone
from globalController import lincolnCinema

bp = Blueprint('customerDashboard', __name__, )

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

def getTheMovies(theID):
    for i in lincolnCinema.allMovie:
        if i.movieID == theID:
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
                return movieInfo

# get the screeninng info and seats
def getTheScreening(theID):
    for s in lincolnCinema.allScreening:
        if s.screeningID == theID:
            screeningInfo = {
                'screeningID': s.screeningID,
                'screeningDate': s.screeningDate,
                'startTime': s.startTime,
                'endTime': s.endTime,
                'cinemaHall': s.cinemaHall.name,
                'status': s.status,
                'id': s.screeningID,
                'seats': s.seats,
                'movieID':s.movie.movieID
            }
            if s.seats:
                # 15 seats for a row, included in a list
                hsList = []
                hs15List = []
                for index, a in enumerate(s.seats):
                    if (index % 15) == 0 and index != 0:
                        hsList.append(hs15List)
                        hs15List = []
                    theSeat = {
                        'col': a.col,
                        'row': a.row,
                        'seatPlace': a.seatPlace,
                        'isReserved': a.isReserved,
                        'seatPrice': a.seatPrice
                    }
                    hs15List.append(theSeat)
                    if index == len(s.seats) - 1:
                        hsList.append(hs15List)
                screeningInfo['seats'] = hsList
            return screeningInfo


@bp.route('/chooseScreening/<int:movieID>')
def chooseScreening(movieID):
    try:
        movie = getTheMovies(movieID)
        return render_template('checkScreening.html', movie=movie)
    except:
        flash('Error, will return to index.','success')
        return redirect('/')

@bp.route('/chooseSeat/<int:screeningID>')
def chooseSeat(screeningID):
    if is_authenticated():
        screening = getTheScreening(screeningID)
        movie = getTheMovies(screening['movieID'])
        return render_template('chooseSeat.html', screening=screening, movie=movie)

    else:
        flash('Error, will return to index.','success')
        return redirect('/')
    




@bp.route('/payment', methods=['POST'])
def payment():
    if is_authenticated():
        selectedSeats = request.form.getlist('theSeat')
        movieID = request.form.get('movieID')
        screeningID = request.form.get('screeningID')

        if not selectedSeats:
            flash('You need to choose at least one seat!','success')
            return redirect(f'/chooseSeat/{screeningID}')

        screening = getTheScreening(int(screeningID))
        movie = getTheMovies(int(movieID))
        session['selectedSeats'] = selectedSeats
        session['movieID'] = int(movieID)
        session['screeningID'] = int(screeningID)
        totalPrice = len(selectedSeats)* 50
        return render_template('payment.html', screening=screening, movie=movie,selectedSeats=selectedSeats, totalPrice=totalPrice)

    else:
        flash('You did not login!', 'success')
        return redirect('/')
    

@bp.route('/paymentProcess', methods=['POST'])
def paymentProcess():
    if is_authenticated():
        screeningID = session['screeningID']
        movieID = session['movieID']
        selectedSeats = session['selectedSeats']
        paymentMethod = request.form.get('paymentMethod')
        username = request.form.get('username')

        cardName = request.form.get('cardName')
        cardNumber = request.form.get('cardNumber')
        cardExp = request.form.get('cardExp')
        cardCVV = request.form.get('cardCVV')

        price = request.form.get('price')

        for s in lincolnCinema.allScreening:
            if s.screeningID == screeningID:
                screening = s
                seatList = s.seats
                seatListCustomer = []
                for i in seatList:
                    for a in selectedSeats:
                        if i.seatPlace == a:
                            seatListCustomer.append(i)
        
        for u in lincolnCinema.allCustomer:
            if u.username == username:
                thisUser = u
        
        payment = {
            'paymentType': paymentMethod, 
            'cardNumber': cardNumber, 
            'cardHolder': cardName, 
            'expiryDate': cardExp, 
            'cvv': cardCVV
        }

        
        makeBookingReturn = lincolnCinema.makeBooking(screening, thisUser, len(selectedSeats), seatListCustomer, payment, price)
        flash(makeBookingReturn, 'success')

        session.pop('selectedSeats')
        session.pop('movieID')
        session.pop('screeningID')

        return redirect('/')

    else:
        flash('You did not login!', 'success')
        return redirect('/')

    


@bp.route('/myBooking')
def myBooking():
    if is_authenticated():
        allBookingList =[]
        for u in lincolnCinema.allCustomer:
            if u.username == session['accountInfo']['username']:
                for b in u.bookingList:
                    theBooking = {
                        'screening': getTheScreening(b.screening.screeningID),
                        'movie': getTheMovies(b.screening.movie.movieID),
                        'seats': [],
                        'status': b.status,
                        'cinemaHall': b.screening.cinemaHall.name,
                        'createdOn':b.createdOn,
                        'bookingID': b.bookingID,
                        'paymentDetail': b.paymentDetail.amount
                    }
                    for s in b.seats:
                        theBooking['seats'].append(s.seatPlace)
                    allBookingList.append(theBooking)


        return render_template('myBooking.html', allBookingList=allBookingList)
    else:
        return redirect('/') 
    

@bp.route('/cancelBooking/<int:bookingID>')
def cancelBooking(bookingID):
    if is_authenticated():

        for u in lincolnCinema.allCustomer:
            if u.username == session['accountInfo']['username']:
                for b in u.bookingList:
                    if b.bookingID == bookingID:
                        removeBookingReturn = lincolnCinema.removeBooking(u,b)
                        flash(removeBookingReturn,'success')
                        return redirect('/myBooking') 


        
    else:
        return redirect('/') 


@bp.route('/msg', methods=['GET'])
def msg():
    allMsg = []
    notiList = lincolnCinema.loggedUser.notiList
    for i in notiList:
        noti = {
            'content': i.content,
            'time':i.date
        }
        allMsg.append(noti)
    return render_template('displayMsg.html', allMsg = reversed(allMsg))

@bp.route('/profile')
def customerProfile():    
    if is_authenticated():
        user = lincolnCinema.loggedUser
       
        customerInfo = {
            'userName': user.username,
            'userPassword': user.userPassword,
            'firstName': user.name,
            'email': user.email,
            'phoneNumber': user.phone,
            'Address': user.address
        } 
        return render_template('customerProfile.html', customerInfo=customerInfo, accountInfo=getAccountInfo())

    else:
        return redirect(url_for('login.login'))    
    
