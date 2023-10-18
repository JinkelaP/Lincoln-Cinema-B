from typing import List
from CinemaMisc import Movie, Screenings
from datetime import datetime
from abc import ABC, abstractmethod


# General class for all users including guests
class General(ABC):


    def searchMovieTitle(self, title: str) -> List[Movie]:
        pass

    def searchMovieRating(self, rating: int) -> List[Movie]:
        pass

    def searchMovieGenre(self, genre: str) -> List[Movie]:
        pass

    def searchMovieDate(self, date: datetime) -> List[Movie]:
        pass

    def viewMovieDetails(self, movie: Movie) -> None:
        pass

# Guest class
class Guest(General):
    def register(self) -> None:
        pass

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
    def __init__(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> None:
        super().__init__(name, address, email, phone)
        self._username = username
        self._password = password

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newPassword):
        self._password = newPassword

    def login(self) -> bool:
        pass

    def logout(self) -> bool:
        pass

    def resetPassword(self) -> bool:
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

    def makeBooking(self) -> bool:
        pass

    def cancelBooking(self) -> bool:
        pass

    def addBookings(self, booking: Booking) -> None:
        self.__bookingList.append(booking)

    def addNoti(self, noti: notification) -> None:
        self.__notiList.append(noti)
