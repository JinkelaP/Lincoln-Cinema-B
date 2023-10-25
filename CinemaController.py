from Generals import Guest, Customer, Admin, FrontDeskStaff
from CinemaMisc import Movie, Screening, Booking, Notification, CinemaHall, CinemaHallSeat, Payment, Coupon, CreditCard, DebitCard, Cash

from decimal import Decimal
from datetime import date, datetime, timedelta

from typing import Union



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
        self.loggedin = 'Guest'

        tempGuest = Guest()
        self.loggedUser = tempGuest


    def login(self, userName: str, psw: str, userType: str) -> str:

        msg = 'Incorrect username or password!'
        if userType == 'Customer':
            for i in self.allCustomer:
                if i.username == userName:
                    if i.login(psw):
                        self.loggedin = 'Customer'
                        self.loggedUser = i
                        return f'Welcome back, {i.name}!'
            else:
                return msg
        elif userType == 'Staff':
            for i in self.allStaff:
                if i.username == userName:
                    if i.login(psw):
                        self.loggedin = 'Staff'
                        self.loggedUser = i
                        return f'Welcome back, {i.name}!'
            else:
                return msg
        elif userType == 'Admin':
            for i in self.allAdmin:
                if i.username == userName:
                    if i.login(psw):
                        self.loggedin = 'Admin'
                        self.loggedUser = i
                        return f'Welcome back, {i.name}!'
            else:
                return msg


    def register(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> str:
        """! register function for the system. Can only register customer. No conficts allowed in username."""
        for i in self.allCustomer:
            if i.username == username:
                return 'Registration failed. The username has been registered.'
        newCustomer = self.loggedUser.register(name, address, email, phone, username, password)
        self.allCustomer.append(newCustomer)
        self.login(username, password)

        return 'You have registered and loggedin!'
    
    def logout(self) -> str:
        tempGuest = Guest()
        self.loggedUser = tempGuest
        self.loggedin = 'Guest'
        return 'You have logged out!'


    def browseAllMovie(self) -> list:
        """! @brief browse all movies in the list."""
        if self.allMovie == []:
            return self.allMovie
        else:
            return self.allMovie.sort(key=lambda movie: movie.releaseDate)

    def searchMovieByStr(self, searching: str) -> list:
        """! Handle all search except date
        @param searching the keyword user is searching"""
        result = []
        for i in self.allMovie:
            if searching in i.title or searching in i.lang or searching in i.genre:
                result.append(i)
        return result

    def searchMovieByDateAfter(self, searching: date) -> list:
        """! Handle date search
        @param searching the date user is searching"""
        result = []
        for i in self.allMovie:
            if i.releaseDate > searching:
                result.append(i)
        if result == []:
            return result
        else:
            return result.sort(key=lambda movie: movie.releaseDate)

    def movieDetail(self, movie: Movie) -> str:
        """! Show the movie detail
        @param movie the movie object user chosed"""
        if movie in self.allMovie:
            return self.loggedUser.viewMovieDetails(movie)
        else:
            return f'Movie not found!'

    def movieSchedule(self, movie: Movie) -> list:
        """! Show the movie screening
        @param movie the movie object user chosed"""
        result = []
        for i in movie.screeningList:
            result.append(i)

        if result == []:
            return result
        else:
            return result.sort(key=lambda screening: screening.screeningDate, reverse=True)

    def checkSeatAvailability(self, screening: Screening) -> list:
        """! Show all seats in the screening
        @param screening the screening object user chosed"""

        return screening.seats

    def makeBooking(self, screening: Screening, user: Customer, numberOfSeats: int, seats: list, payment: dict, price: Decimal, coupon: Coupon = None) -> str:
        # payment = {paymentType, cardNumber: str, cardHolder: str, expiryDate: date}
        
        """! Make a booking, creating the ticket
        @param screening the screening user chosed
        @param user the customer
        @param seatID the seat customer chosed
        @param paymentType could be cash or card
        @param price could apply coupon"""
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


        newBooking = Booking(user, screening, True, numberOfSeats, price, paymentNew)
        for i in seats:
            i.isReserved = False
            newBooking.addSeat(i)

        user.addBookings(newBooking)
        msg = f'You have successfully purchased the ticket!'
        user.addNoti(Notification(user, msg))
        return msg

    def removeBooking(self, user: Customer, ticket: Booking) -> str:
        """! deactivate a ticket
        @param user the customer
        @param ticket the ticket"""

        ticket.status = False
        for i in ticket.seats:
            i.isReserved = False

        msg = f'You have successfully cancelled the tickets!'
        user.addNoti(Notification(user, msg))
        return msg

    def addMovie(self, title: str, description: str, durationMin: int, language: str, releaseDate: datetime, country: str, genre: str) -> str:
        """! add a movie to the list
    @param name The name of the movie.
    @param langauge The language of the movie.
    @param genre The genre of the movie (e.g., action, drama).
    @param releaseDate The official release date of the movie.
    @param duration The duration of the movie in minutes."""
        newMovie = Movie(title, description, durationMin, language, releaseDate, country, genre)
        self.allMovie.append(newMovie)
        msg = f'You have successfully added a movie!'
        return msg

    
    def addScreening(self, movie: Movie, dateT: datetime, hallName: str) -> str:
        """! add a movie screening
        @param movie the movie
        @param dateT the start datetime
        @param hall the hall"""
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
                    newScreening = Screening(movie, dateT.date(), dateT, dateTEnd, i, hallSeat)
                    self.allScreening.append(newScreening)
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
        """! remove a movie, including screenings
        @param movie the movie"""
        # remove movie + deactivate screenings
        movie.status = False

        for i in self.allScreening:
            if i.movie == movie:
                self.removeScreening(i)

        return 'Movie removed. Screenings cancelled (if available).'

    
    def removeScreening(self, screening: Screening) -> str:
        """! remove a screening, including refund.
        @param screening the screening"""

        screening.status = False
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
        """@param msg the message"""
        self.publicMsg.append([datetime.now(), msg])
        return 'Public message sent!'
