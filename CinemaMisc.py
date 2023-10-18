from datetime import datetime
from typing import List
from General import Customer, User
from abc import ABC, abstractmethod

# Movie class
class Movie:
    def __init__(self, title: str, description: str, duration: int, language: str, releaseDate: datetime, country: str, genre: str):
        self.__title = title
        self.__description = description
        self.__duration = duration
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
    def duration(self):
        return self.__duration

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

    def getScreenings(self) -> List["Screening"]:
        return self.screeningList

# Screening class
class Screening:
    def __init__(self, movie: Movie, screeningDate: datetime):
        self.__movie = movie
        self.__screeningDate = screeningDate
        self.__cinemaHall: CinemaHall = None

    @property
    def movie(self):
        return self.__movie

    @property
    def screeningDate(self):
        return self.__screeningDate

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

    def sendNotification(self) -> "Notification":
        # This is a placeholder. You'll need to implement the actual notification mechanism.
        notification = Notification(self.customer, "Your booking is confirmed!")
        return notification

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

# CinemaHallSeat class
class CinemaHallSeat:
    def __init__(self, seatNumber: int, row: int, seatType: str, isReserved: bool, seatPrice: float):
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

    def paymentDone(self) -> bool:
        raise NotImplementedError("This method should be implemented in child classes.")

    def calcFinalAmount(self) -> float:
        # This method might include logic to calculate final amount after applying any discounts, taxes etc.
        # Placeholder for now
        return self.amount

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
        # Implement the actual debit card payment mechanism here
        # Placeholder for now
        return True

# CreditCard class
class CreditCard(Payment):
    def __init__(self, amount: float, cardNumber: str, cardHolder: str, expiryDate: datetime):
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
        # Implement the actual credit card payment mechanism here
        # Placeholder for now
        return True
