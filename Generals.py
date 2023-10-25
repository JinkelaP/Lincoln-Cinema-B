from typing import List
from CinemaMisc import Movie, Screening
from datetime import datetime
from abc import ABC, abstractmethod


# General class for all users including guests
class General(ABC):


    def searchMovieTitle(self, title: str) -> List[Movie]:
        pass

    def searchMovieLang(self, Lang: str) -> List[Movie]:
        pass

    def searchMovieGenre(self, genre: str) -> List[Movie]:
        pass

    def searchMovieDate(self, date: datetime) -> List[Movie]:
        pass

    def viewMovieDetails(self, movie: Movie) -> None:
        return f'Title: {movie.title}\nLanguage: {movie.language}\nGenre: {movie.genre}\nDate of Release: {movie.releaseDate}\nDuration: {movie.durationMin}'

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
