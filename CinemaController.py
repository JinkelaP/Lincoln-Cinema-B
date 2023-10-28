from Generals import Guest, Customer, Admin, FrontDeskStaff, Movie, Screening, Booking, Notification, CinemaHall, CinemaHallSeat, Payment, Coupon, CreditCard, DebitCard, Cash
from decimal import Decimal
from datetime import date, datetime, timedelta
from typing import Union

import random

class Cinema:
    """! The controller of the cinema management sys."""

    def __init__(self) -> None:
        """! Constructor for the controller."""
        self.allCustomer = []
        self.allStaff = []
        self.allAdmin = []

        self.allHall = [CinemaHall('H1', 120), CinemaHall('H2', 90), CinemaHall('H3', 110), CinemaHall('H4', 80)]
        # self.allHall = []
        self.allMovie = []
        self.allScreening = []
        self.publicMsg = []
        self.loggedin = None
        self.readFileStatus = None

        tempGuest = Guest()
        self.loggedUser = tempGuest
        
    def readFile(self):
        try:
            
            if self.readFileStatus != True:

                adminFile = open("AdminData.txt", "r")
                for line in adminFile:
                    data = line.strip()
                    data = data.split(",")
                    adminObject = (data[0], data[1], data[2], data[3], data[4], data[5])
                    self.allAdmin.append(adminObject)
                
                staffFile = open("StaffData.txt", "r")
                for line in staffFile:
                    data = line.strip()
                    data = data.split(",")
                    staffObject = (data[0], data[1], data[2], data[3], data[4], data[5])
                    self.allStaff.append(staffObject)

                movieFile = open("MovieData.txt", "r")
                for line in movieFile:
                    data = line.strip()
                    data = data.split(",")
                    movieObject = Movie(data[0], data[1], int(data[2]), data[3], datetime.fromisoformat(data[4]).date(), data[5], data[6])
                    self.allMovie.append(movieObject)
                self.addScreening(self.allMovie[0], datetime.now() + timedelta(days=2), 'H2')
                self.addScreening(self.allMovie[1], datetime.now() + timedelta(days=5), 'H1')
                self.addScreening(self.allMovie[2], datetime.now() + timedelta(days=4), 'H3')
            
                self.readFileStatus = True
                return {'Status': 'Done'}
            
            else:
                return {'Status': 'Has read'}


        except Exception as e:
            return {'Status': 'Error'}


    def login(self, userName: str, psw: str, userType: str) -> str:

        msgFail = 404
        if userType == 'Customer':
            for i in self.allCustomer:
                if i.username == userName:
                    if i.login(psw):
                        self.loggedin = 'Customer'
                        self.loggedUser = i
                        return self.loggedUser.name
            else:
                return msgFail
        elif userType == 'Staff':
            for i in self.allStaff:
                if i.username == userName:
                    if i.login(psw):
                        self.loggedin = 'Staff'
                        self.loggedUser = i
                        return self.loggedUser.name
            else:
                return msgFail
        elif userType == 'Admin':
            for i in self.allAdmin:
                if i.username == userName:
                    if i.login(psw):
                        self.loggedin = 'Admin'
                        self.loggedUser = i
                        return self.loggedUser.name
            else:
                return msgFail


    def register(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> str:
        """! register function for the system. Can only register customer. No conficts allowed in username."""
        for i in self.allCustomer:
            if i.username == username:
                return 'Conflict'
        newCustomer = self.loggedUser.register(name, address, email, phone, username, password)
        self.allCustomer.append(newCustomer)
        self.login(username, password)

        return 'You have registered and loggedin!'
    
    def logout(self) -> str:
        tempGuest = Guest()
        self.loggedUser = tempGuest
        self.loggedin = None
        return 'You have logged out!'


    def browseAllMovie(self) -> list:
        """! @brief browse all movies in the list."""
        if self.allMovie == []:
            return self.allMovie
        else:
            return self.allMovie.sort(key=lambda movie: movie.releaseDate)

    def searchMovieByStr(self, searching: str) -> list:
        """! Handle all search except date"""
        return self.loggedUser.searchMovieTitleLangGenre(searching, self.allMovie)

    def searchMovieByDateAfter(self, searching: date) -> list:
        """! Handle date search"""
        return self.loggedUser.searchMovieDate(searching, self.allMovie)
        

    def movieDetail(self, movie: Movie) -> dict:
        """! Show the movie detail
        """
        if movie in self.allMovie:
            return self.loggedUser.viewMovieDetails(movie)
        else:
            return {'status': 404}

    def movieSchedule(self, movie: Movie) -> list:
        """! Show the movie screening
        """
        result = []
        for i in movie.screeningList:
            result.append(i)

        if result == []:
            return result
        else:
            return result.sort(key=lambda screening: screening.screeningDate, reverse=True)

    def checkSeatAvailability(self, screening: Screening) -> list:
        """! Show all seats in the screening
        """

        return screening.seats

    def makeBooking(self, screening: Screening, user: Customer, numberOfSeats: int, seats: list, payment: dict, price: Decimal, coupon: Coupon = None) -> str:
        # payment = {paymentType: str, cardNumber: str, cardHolder: str, expiryDate: date}
        
        """! Make a booking, creating the ticket"""

        # create the ticket + put it in user's list + mark unavailable in screening

        if coupon:
            if coupon.expiryDate >= date.now():
                price -= coupon.discount
            else:
                return 'Invalid Coupon'

        if payment['paymentType'] == 'credit':
            paymentNew = CreditCard(price, payment['cardNumber'], payment['cardHolder'], payment['expiryDate'])
        elif payment['paymentType'] == 'debit':
            paymentNew = DebitCard(price, payment['cardNumber'], payment['cardHolder'], payment['expiryDate'])
        else:
            paymentNew = Cash(price)

        newBooking = self.loggedUser.makeBooking(user, screening, numberOfSeats, price, paymentNew)

        for i in seats:
            i.isReserved = False
            newBooking.addSeat(i)

        user.addBookings(newBooking)
        msg = f'You have successfully purchased the ticket!'
        user.addNoti(Notification(user, msg))
        return msg

    def removeBooking(self, user: Customer, ticket: Booking) -> str:
        """! deactivate a ticket"""
        self.loggedUser.cancelBooking(ticket)

        msg = f'You have successfully cancelled the tickets!'
        user.addNoti(Notification(user, msg))
        return msg

    def addMovie(self, title: str, description: str, durationMin: int, language: str, releaseDate: datetime, country: str, genre: str) -> str:
        """! add a movie to the list"""
        if self.loggedin == 'Admin':
            self.loggedUser.addMovie(title, description, durationMin, language, releaseDate, country, genre, self.allMovie)
        
        msg = f'You have successfully added a movie!'
        return msg

    
    def addScreening(self, movie: Movie, dateT: datetime, hallName: str) -> str:
        """! add a movie screening"""
        # validate datetime conflicts, generate seats
        dateTEnd = dateT + timedelta(minutes=movie.durationMin)
        for i in self.allScreening:
            if dateT < i.endTime and dateTEnd > i.startTime:
                if i.CinemaHall.name == hallName:
                    return 'Creat screening failed. Time Conflicts detected.'
        else:
            for i in self.allHall:
                if i.name == hallName:
                    hallSeat = self.hallSeatCreate(i)
                    self.loggedUser.addScreening(movie, dateT.date(), dateT, dateTEnd, i, hallSeat, self.allScreening)
                    
                    return 'Creat screening success.'
    
    def hallSeatCreate(hall: CinemaHall, priceTicket) -> list:
        """!@brief create seats in the screening hall"""
        maxRow = 15
        nowRow = 1
        nowCol = 'A'

        result = []
        for i in range(hall.totalSeats):
            if nowRow <= maxRow:
                result.append(CinemaHallSeat(nowCol, nowRow, False, priceTicket))
            else:
                nowRow = 1
                nowCol = chr(ord(nowCol) + 1)
                result.append(CinemaHallSeat(nowCol, nowRow, False, priceTicket))
            nowRow += 1

        return result

    
    def removeMovie(self, movie: Movie) -> str:
        """! remove a movie, including screenings"""
        # remove movie + deactivate screenings
        self.loggedUser.cancelMovie(movie)

        for i in self.allScreening:
            if i.movie == movie:
                self.removeScreening(i)

        return 'Movie removed. Screenings cancelled (if available).'

    
    def removeScreening(self, screening: Screening) -> str:
        """! remove a screening, including refund.
        """

        self.loggedUser.cancelScreening(screening)
        for a in screening.seats:
            if type(a.userID) == int:
                for user in self.allCustomer:
                    if user.userID == a.userID:
                        user.addNoti(user, f'The screening your booked on {screening.screeningDate.strftime("%d-%m-%Y")} has been cancelled.')
                        for ticket in user.bookingList:
                            if ticket.screening == screening:
                                ticket.status = False

        return 'Screening cancelled. Customers has been notified.'


    def sendPublicMsg(self, msg: str) -> str:

        self.publicMsg.append([datetime.now(), msg])
        return 'Public message sent!'
