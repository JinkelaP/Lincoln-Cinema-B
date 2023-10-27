from typing import List
from abc import ABC, abstractmethod
from datetime import datetime, date
from decimal import Decimal

# General class for all users including guests


class General(ABC):

    def searchMovieTitleLangGenre(self, searching: str, movieList: List['Movie']) -> List['Movie']:
        result = []
        for i in movieList:
            if searching in i.title or searching in i.lang or searching in i.genre:
                result.append(i)
        return result


    def searchMovieDate(self, date: datetime) -> List['Movie']:
        pass

    def viewMovieDetails(self, movie: ['Movie']) -> None:
        movieInfo = {
            'title': movie.title, 
            'language': movie.language, 
            'genre': movie.genre,
            'releaseDate': movie.releaseDate, 
            'durationMin': movie.durationMin
            }
        return movieInfo

# Guest class


class Guest(General):
    def register(self, name, address, email, phone, username, password) -> ['Customer']:
        newCustomer = Customer(name, address, email, phone, username, password)
        return newCustomer

# Person class with basic info


class Person(General, ABC):
    def __init__(self, name: str, address: str, email: str, phone: str) -> None:
        self._name = name
        self._address = address
        self._email = email
        self._phone = phone

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def email(self):
        return self._email

    @property
    def phone(self):
        return self._phone

# User


class User(Person, ABC):  # inherit
    nextID = 100

    def __init__(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> None:
        super().__init__(name, address, email, phone)
        self._username = username
        self._userPassword = password
        self._userID = User.nextID
        User.nextID += 1

    @property
    def username(self):
        return self._username

    @property
    def userPassword(self):
        return self._password

    @userPassword.setter
    def userPassword(self, newPassword):
        self._password = newPassword

    def login(self, psw: str) -> bool:
        if psw == self._userPassword:
            return True

    def logout(self) -> bool:
        pass

# Admin class


class Admin(User):
    def addMovie(self) -> bool:
        pass

    def addScreening(self) -> bool:
        pass

    def cancelMovie(self) -> bool:
        pass

    def cancelScreening(self) -> bool:
        pass

# FrontDeskStaff class


class FrontDeskStaff(User):
    def makeBooking(self) -> bool:
        pass

    def cancelBooking(self) -> bool:
        pass

# Customer class


class Customer(User):
    def __init__(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> None:
        super().__init__(name, address, email, phone, username, password)
        self.__bookingList = []
        self.__notiList = []

    @property
    def bookingList(self):
        return self.__bookingList

    @property
    def notiList(self):
        return self.__notiList

    def addBookings(self, booking: ['Booking']) -> None:
        self.__bookingList.append(booking)

    def addNoti(self, noti: ['notification']) -> None:
        self.__notiList.append(noti)


# Movie class
class Movie:
    def __init__(self, title: str, description: str, durationMin: int, language: str, releaseDate: datetime, country: str, genre: str):
        self.__title = title
        self.__description = description
        self.__durationMin = durationMin
        self.__language = language
        self.__releaseDate = releaseDate
        self.__country = country
        self.__genre = genre
        self.__screeningList: List[Screening] = []
        self.__status = True

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def durationMin(self):
        return self.__durationMin

    @property
    def language(self):
        return self.__language

    @property
    def releaseDate(self):
        return self.__releaseDate

    @property
    def country(self):
        return self.__country

    @property
    def genre(self):
        return self.__genre

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, i: bool):
        self.__status = i

    @property
    def screeningList(self):
        return self.__screeningList


# Screening class
class Screening:
    def __init__(self, movie: Movie, screeningDate: date, startTime: datetime, endTime: datetime, hall: 'CinemaHall'):
        self.__movie = movie
        self.__screeningDate = screeningDate
        self.__startTime = startTime
        self.__endTime = endTime
        self.__cinemaHall: CinemaHall = None
        self.__seats: List[CinemaHallSeat] = []
        self.__status = True

    @property
    def movie(self):
        return self.__movie

    @property
    def screeningDate(self):
        return self.__screeningDate

    @property
    def startTime(self):
        return self.__startTime

    @property
    def endTime(self):
        return self.__endTime

    @property
    def cinemaHall(self):
        return self.__cinemaHall

    @property
    def seats(self):
        return self.__seats

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, i: bool):
        self.__status = i

    def addSeat(self, seats: ['CinemaHallSeat']) -> None:
        self.__seats.append(seats)


# Booking class
class Booking:
    nextID = 10000

    def __init__(self, customer: Customer, screening: Screening, status: bool, numberOfSeats: int, orderTotal: Decimal, paymentDetail: Payment):

        self.__bookingNum = Booking.nextID
        self.__customer = customer
        self.__screening = screening
        self.__numberOfSeats = numberOfSeats
        self.__status = status
        self.__orderTotal = orderTotal
        self.__paymentDetail = paymentDetail
        self.__createdOn = datetime.now()
        self.__seats: List[CinemaHallSeat] = []
        Booking.nextID += 1

    @property
    def bookingNum(self):
        return self.__bookingNum

    @property
    def customer(self):
        return self.__customer

    @property
    def screening(self):
        return self.__screening

    @property
    def numberOfSeats(self):
        return self.__numberOfSeats

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, i):
        self.__status = i

    @property
    def orderTotal(self):
        return self.__orderTotal

    @property
    def paymentDetail(self):
        return self.__paymentDetail

    @property
    def createdOn(self):
        return self.__createdOn

    @property
    def seats(self):
        return self.__seats

    @seats.setter
    def status(self, status: bool):
        self.status = status

    def addSeat(self, seats: ['CinemaHallSeat']) -> None:
        self.__seats.append(seats)

    def sendNotification(self) -> None:
        notification = Notification(
            self.customer, f"Your booking of {self.__screening.screeningDate} is confirmed!")


# Notification class
class Notification:
    def __init__(self, customer: Customer, content: str):
        self.__customer = customer
        self.__date = datetime.now()
        self.__content = content

    @property
    def customer(self):
        return self.__customer

    @property
    def date(self):
        return self.__date

    @property
    def content(self):
        return self.__content

# CinemaHall class


class CinemaHall:
    def __init__(self, name: str, totalSeats: int):
        self.__name = name
        self.__totalSeats = totalSeats
        # self.__seats: List[CinemaHallSeat] = []

    @property
    def name(self):
        return self.__name

    @property
    def totalSeats(self):
        return self.__totalSeats

    # @property
    # def seats(self):
    #     return self.__seats

    # @seats.setter
    # def seats(self, seatList):
    #     if seatList is List[CinemaHallSeat]:
    #         self.__seats = seatList

# CinemaHallSeat class


class CinemaHallSeat:
    def __init__(self, col: str, row: int, isReserved: bool, seatPrice: Decimal):
        self.__col = col
        self.__row = row
        self.__isReserved = isReserved
        self.__seatPrice = seatPrice
        self.__userID = None

    @property
    def col(self):
        return self.__col

    @property
    def row(self):
        return self.__row

    @property
    def isReserved(self):
        return self.__isReserved

    @property
    def seatPrice(self):
        return self.__seatPrice

    @property
    def userID(self):
        return self.__userID

    @userID.setter
    def userID(self, id):
        self.__userID = id

    @isReserved.setter
    def isResearved(self, status: bool):
        self.__isReserved = status


# Abstract Payment class
class Payment(ABC):
    def __init__(self, amount: float):
        self._amount = amount
        self._date = datetime.now()

    @property
    def amount(self):
        return self._amount

    @property
    def date(self):
        return self._date

    @abstractmethod
    def paymentDone(self) -> bool:
        pass

    # def calcFinalAmount(self) -> float:
    #     # This method might include logic to calculate final amount after applying any discounts, taxes etc.
    #     # Placeholder for now
    #     return self.amount

# Coupon class


class Coupon:
    def __init__(self, couponId: str, discount: int, expiryDate: date):
        self.__couponId = couponId
        self.__expiryDate = expiryDate
        self.__discount = discount

    @property
    def couponId(self):
        return self.__couponId

    @property
    def discount(self):
        return self.__discount

    @property
    def expiryDate(self):
        return self.__expiryDate

# DebitCard class


class DebitCard(Payment):
    def __init__(self, amount: Decimal, cardNumber: str, cardHolder: str):
        super().__init__(amount)
        self.__cardNumber = cardNumber
        self.__cardHolder = cardHolder

    @property
    def cardNumber(self):
        return self.__cardNumber

    @property
    def cardHolder(self):
        return self.__cardHolder

    def paymentDone(self) -> bool:
        return True

# CreditCard class


class CreditCard(Payment):
    def __init__(self, amount: Decimal, cardNumber: str, cardHolder: str, expiryDate: date):
        super().__init__(amount)
        self.__cardNumber = cardNumber
        self.__cardHolder = cardHolder
        self.__expiryDate = expiryDate

    @property
    def cardNumber(self):
        return self.__cardNumber

    @property
    def cardHolder(self):
        return self.__cardHolder

    @property
    def expiryDate(self):
        return self.__expiryDate

    def paymentDone(self) -> bool:
        return True

# Cash class

# CreditCard class


class Cash(Payment):
    def __init__(self, amount: Decimal):
        super().__init__(amount)

    def paymentDone(self) -> bool:
        return True
