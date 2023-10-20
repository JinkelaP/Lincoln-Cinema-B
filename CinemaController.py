from Generals import Guest, Customer, Admin, FrontDeskStaff
from CinemaMisc import Movie, Screening, Booking, Notification, CinemaHall, CinemaHallSeat, Payment, Coupon, CreditCard, DebitCard

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
                    if i.userPassword == psw:
                        self.loggedin = 'Customer'
                        self.loggedUser = i
                        return f'Welcome back, {i.name}!'
            else:
                return msg
        elif userType == 'Staff':
            for i in self.allStaff:
                if i.username == userName:
                    if i.userPassword == psw:
                        self.loggedin = 'Staff'
                        self.loggedUser = i
                        return f'Welcome back, {i.name}!'
            else:
                return msg
        elif userType == 'Admin':
            for i in self.allAdmin:
                if i.username == userName:
                    if i.userPassword == psw:
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
            if searching in i.movieName or searching in i.lang or searching in i.genre:
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
            return f'Title: {movie.movieName}\nLanguage: {movie.lang}\nGenre: {movie.genre}\nDate of Release: {movie.releaseDate}\nDuration: {movie.duration}'
        else:
            return f'Movie not found!'

    def movieSchedule(self, movie: Movie) -> list:
        """! Show the movie screening
        @param movie the movie object user chosed"""
        result = []
        for i in self.allScreening:
            if i.movieID == movie.movieID:
                result.append(i)

        if result == []:
            return result
        else:
            return result.sort(key=lambda screening: screening.dateT, reverse=True)

    def checkSeatAvailability(self, screening: Screening) -> list:
        """! Show all seats in the screening
        @param screening the screening object user chosed"""
        return screening.hallSeat

    def makeBooking(self, screening: Screening, user: Customer, seatID: str, paymentType: str, price: Decimal, coupon=None) -> str:
        """! Make a booking, creating the ticket
        @param screening the screening user chosed
        @param user the customer
        @param seatID the seat customer chosed
        @param paymentType could be cash or card
        @param price could apply coupon"""
        # create the ticket + put it in user's list + mark unavailable in screening

        if coupon:
            price = price * coupon.discount * 0.01
            user.removeCoupon(coupon)

        newTicket = Ticket(user.userID, Screening.screeningID,
                           datetime.now, seatID, paymentType, price)

        user.addTicket(newTicket)
        screening.markSeatFalse(seatID, user.userID)
        msg = f'You have successfully purchased a ticket! No. {newTicket.ticketID}'
        user.userMsgAdd(msg)
        return msg

    def removeTicket(self, user: Customer, ticket: Ticket) -> str:
        """! deactivate a ticket
        @param user the customer
        @param ticket the ticket"""
        for i in user.coupon:
            if i == ticket:
                user.removeTicket(ticket)
                break

        msg = f'You have successfully cancelled a ticket!'
        user.userMsgAdd(msg)
        return msg

    def addMovie(self, name: str, langauge: str, genre: str, releaseDate: date, duration: int) -> str:
        """! add a movie to the list
    @param name The name of the movie.
    @param langauge The language of the movie.
    @param genre The genre of the movie (e.g., action, drama).
    @param releaseDate The official release date of the movie.
    @param duration The duration of the movie in minutes."""
        newMovie = Movie(name, langauge, genre, releaseDate, duration)
        self.allMovie.append(newMovie)
        msg = f'You have successfully added a movie!'
        return msg

    
    def hallSeatCreate(hall: Hall) -> list:
        """!@brief create seats in the screening hall"""
        maxRow = 15
        nowRow = 1
        nowCol = 'A'

        result = []
        for i in range(hall.hallCapacity):
            if nowRow <= maxRow:
                result.append(Seat(nowCol, nowRow))
            else:
                nowRow = 1
                nowCol = chr(ord(nowCol) + 1)
                result.append(Seat(nowCol, nowRow))
            nowRow += 1

        return result

    
    def addScreening(self, movie: Movie, dateT: datetime, hall: Hall) -> str:
        """! add a movie screening
        @param movie the movie
        @param dateT the start datetime
        @param hall the hall"""
        # validate datetime conflicts, generate seats
        datetEndPlus = ((movie.duration / 30) + 1) * 30
        dateTEnd = dateT + timedelta(minutes=datetEndPlus)
        for i in self.allScreening:
            if dateT < i.dateTEnd and dateTEnd > i.dateT:
                if i.hallID == hall.hallID:
                    return 'Creat screening failed. Time Conflicts detected.'
        else:
            hallSeat = self.hallSeatCreate(hall)
            newScreening = Screening(
                movie.movieID, dateT, dateTEnd, hall.hallID, hallSeat)
            return 'Creat screening success.'

    
    def removeMovie(self, movie: Movie) -> str:
        """! remove a movie, including screenings
        @param movie the movie"""
        # remove movie + deactivate screenings
        movieID = movie.movieID
        if movie in self.allMovie:
            self.allMovie.remove(movie)

        for i in self.allScreening:
            if i.movieID == movieID:
                self.removeScreening(i)

        return 'Movie removed. Screenings cancelled (if available).'

    
    def removeScreening(self, screening: Screening) -> str:
        """! remove a screening, including refund.
    @param screening the screening"""
        for i in self.allScreening:
            if i == screening:
                i.valid = False
                for a in i.hallSeat:
                    if type(a.userID) is int:
                        for user in self.allCustomer:
                            if user.userID == a.userID:
                                user.userMsgAdd(
                                    f'The screening your booked on {screening.dateT.strftime("%d-%m-%Y, %H:%M")} has been cancelled.')
                                for ticket in user.ticket:
                                    if ticket.screeningID == screening.screeningID:
                                        ticket.valid = False

        return 'Screening cancelled. Customers has been notified.'

    
    def isValidCoupon(coupon: Coupon) -> bool:
        """! check if a coupon is valid
        @param coupon the coupon"""
        if coupon.valid != True or coupon.expireDate < datetime.now().date():
            return False
        else:
            return True
        
    def sendPublicMsg(self, msg: str) -> str:
        """! check if a coupon is valid
        @param msg the message"""
        self.publicMsg.append([datetime.now(), msg])
        return 'Public message sent!'
