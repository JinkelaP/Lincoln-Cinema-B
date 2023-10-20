from datetime import datetime, date
from typing import List
from Generals import Customer, User
from abc import ABC, abstractmethod
from decimal import Decimal

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

# Booking class
class Booking:
    def __init__(self, bookingNum: str, customer: Customer, screening: Screening):
        self.__bookingNum = bookingNum
        self.__customer = customer
        self.__screening = screening
        self.__date = datetime.now()
        self.__seats: List[CinemaHallSeat] = []

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
    def date(self):
        return self.__date

    @property
    def seats(self):
        return self.__seats

    def sendNotification(self) -> None:

        notification = Notification(self.customer, f"Your booking of {self.__screening.screeningDate} is confirmed!")


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
        self.__seats: List[CinemaHallSeat] = []

    @property
    def name(self):
        return self.__name

    @property
    def totalSeats(self):
        return self.__totalSeats

    @property
    def seats(self):
        return self.__seats
    
    @seats.setter
    def seats(self, seatList):
        if seatList is List[CinemaHallSeat]:
            self.__seats = seatList

# CinemaHallSeat class
class CinemaHallSeat:
    def __init__(self, seatNumber: int, row: int, seatType: str, isReserved: bool, seatPrice: Decimal):
        self.__seatNumber = seatNumber
        self.__row = row
        self.__seatType = seatType
        self.__isReserved = isReserved
        self.__seatPrice = seatPrice

    @property
    def seatNumber(self):
        return self.__seatNumber

    @property
    def row(self):
        return self.__row

    @property
    def seatType(self):
        return self.__seatType

    @property
    def isReserved(self):
        return self.__isReserved

    @property
    def seatPrice(self):
        return self.__seatPrice

    

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
    def __init__(self, couponId: str, discount: float):
        self.__couponId = couponId
        self.__discount = discount

    @property
    def couponId(self):
        return self.__couponId

    @property
    def discount(self):
        return self.__discount

# DebitCard class
class DebitCard(Payment):
    def __init__(self, amount: float, cardNumber: str, cardHolder: str):
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
    def __init__(self, amount: float, cardNumber: str, cardHolder: str, expiryDate: date):
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
