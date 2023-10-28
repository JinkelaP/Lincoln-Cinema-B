from Generals import Guest, Customer, Admin, FrontDeskStaff, Movie, Screening, Booking, Notification, CinemaHall, CinemaHallSeat, Payment, Coupon, CreditCard, DebitCard, Cash
from decimal import Decimal
from datetime import date, datetime, timedelta
from typing import Union

import pytest

movies = [
    Movie("LincolnUniMovie", "Academic Film Assignment", 150, "English", datetime.now() - timedelta(days=365), "USA", "Action"),
    Movie("WigramFight", "Lifestyle in Wigram but abnormal", 150, "English", datetime.now(), "USA", "Sci-Fi"),
    Movie("HAHAHAHAHHAHAHA", "Documentary internet meme", 112, "French", datetime.now() - timedelta(days=2000), "France", "Drama"),
]


class TestGeneral:
    def setup_method(self):
        self.general = Guest()

    def test_searchMovieTitleLangGenre(self):
        result = self.general.searchMovieTitleLangGenre("LincolnUniMovie", movies)
        assert len(result) == 1
        assert result[0].title == "LincolnUniMovie"

        # test if not existing
        result = self.general.searchMovieTitleLangGenre("NotExistingTitle", movies)
        assert len(result) == 0

    def test_searchMovieDate(self):
        result = self.general.searchMovieDate(datetime.now() - timedelta(days=1000), movies)
        assert len(result) == 2

        # test order
        assert result[0].title == "WigramFight"
        assert result[1].title == "LincolnUniMovie"

    def test_viewMovieDetails(self):
        movie = movies[0]
        result = self.general.viewMovieDetails(movie)
        assert result['title'] == "LincolnUniMovie"
        assert result['language'] == "English"


class TestGuest:
    def setup_method(self):
        self.guest = Guest()

    def test_register(self):
        name = "John Biden"
        address = "12345 Main South Rd"
        email = "johnthepresident@gmail.com"
        phone = "0220220222"
        username = "johnbiden"
        password = "securepassword"

        customer = self.guest.register(name, address, email, phone, username, password)

        assert isinstance(customer, Customer)

        # customer info
        assert customer.name == name
        assert customer.address == address
        assert customer.email == email
        assert customer.phone == phone
        assert customer.username == username
        assert customer.userPassword == password


class TestUser:
    # Since user is an abstract class, admin is used for testing.
    def setup_method(self):
        self.admin = Admin(
            "John Biden",
            "12345 Main South Rd",
            "johnthepresident@gmail.com",
            "0220220222",
            "johnbiden",
            "securepassword"
        )

    def test_initialization(self):
        assert self.admin.name == "John Biden"
        assert self.admin.address == "12345 Main South Rd"
        assert self.admin.email == "johnthepresident@gmail.com"
        assert self.admin.phone == "0220220222"
        assert self.admin.username == "johnbiden"
        assert self.admin.userPassword == "securepassword"

    def test_login(self):
        assert self.admin.login("securepassword")
        assert not self.admin.login("wrongpassword")



###################################
class MockMovie:
    def __init__(self, title):
        self.title = title
        self.status = True

class TestUserBooking:

    def setup_method(self):
        self.user = Customer(
            "John Biden",
            "12345 Main South Rd",
            "johnthepresident@gmail.com",
            "0220220222",
            "johnbiden",
            "securepassword"
        )
        self.mock_movie = MockMovie('Haha')
        self.mock_screening = Screening(self.mock_movie, date.today(), datetime.now(), datetime.now() + timedelta(hours=2), None,[])
        self.mock_payment = Payment(Decimal(20.0))
        self.mock_seat1 = CinemaHallSeat("A", 1, False, Decimal(10.0))
        self.mock_seat2 = CinemaHallSeat("A", 2, False, Decimal(10.0))
        

    def test_makeBooking(self):
        booking = self.user.makeBooking(self.user, self.mock_screening, 2, Decimal(20.0), self.mock_payment)
        booking.addSeat(self.mock_seat1)
        booking.addSeat(self.mock_seat2)
        assert isinstance(booking, Booking)
        assert booking.customer == self.user
        assert booking.screening == self.mock_screening
        assert booking.numberOfSeats == 2
        assert booking.orderTotal == Decimal(20.0)
        assert booking.paymentDetail == self.mock_payment
        assert booking.status


    def test_cancelBooking(self):
        booking = self.user.makeBooking(self.user, self.mock_screening, 2, Decimal(20.0), self.mock_payment)
        booking.addSeat(self.mock_seat1)
        booking.addSeat(self.mock_seat2)
        assert booking.status
        self.user.cancelBooking(booking)
        assert not booking.status


#######################################################
class TestAdmin:
    def setup_method(self):
        self.admin = Admin(
            "John Biden",
            "12345 Main South Rd",
            "johnthepresident@gmail.com",
            "0220220222",
            "johnbiden",
            "securepassword"
        )
        self.all_movies = []
        self.all_screenings = []

    def test_addMovie(self):
        movie = self.admin.addMovie("LincolnUniMovie", "Description", 120, "English", date(2010, 7, 16), "USA", "Sci-Fi", self.all_movies)
        assert movie in self.all_movies
        assert movie.title == "LincolnUniMovie"

    def test_addScreening(self):
        movie = MockMovie("LincolnUniMovie")
        screening = self.admin.addScreening(movie, date.today(), datetime.now(), datetime.now() + timedelta(hours=2), None, [], self.all_screenings)
        assert screening in self.all_screenings
        assert screening.movie == movie

    def test_cancelMovie(self):
        movie = MockMovie("LincolnUniMovie")
        self.all_movies.append(movie)
        assert movie.status
        self.admin.cancelMovie(movie)
        assert not movie.status

    def test_cancelScreening(self):
        movie = MockMovie("LincolnUniMovie")
        screening = Screening(movie, date.today(), datetime.now(), datetime.now() + timedelta(hours=2), None,[])
        self.all_screenings.append(screening)
        assert screening.status
        self.admin.cancelScreening(screening)
        assert not screening.status

#########################
class TestCustomer:

    def setup_method(self):
        self.customer = Customer("John Biden", "12345 Main South Rd", "johnthepresident@gmail.com", "0220220222", "johndoe", "password")
    
    def test_addBooking(self):
        # Mock data
        payment = Payment(Decimal(100.0))
        screening = Screening(MockMovie('haha'), date.today(), datetime.now(), datetime.now() + timedelta(hours=2), CinemaHall('H1',100),[]) 
        seat = CinemaHallSeat("A", 1, False, Decimal(50.0))
        
        booking = Booking(self.customer, screening, True, 1, Decimal(50.0), payment)
        booking.addSeat(seat)
        
        self.customer.addBookings(booking)
        
        assert len(self.customer.bookingList) == 1
        assert self.customer.bookingList[0].screening == screening
        assert self.customer.bookingList[0].seats[0] == seat

    def test_addNotification(self):
        # Mock data
        notification_content = "Your booking has been confirmed!"
        noti = Notification(self.customer, notification_content)

        self.customer.addNoti(noti)

        assert len(self.customer.notiList) == 1
        assert self.customer.notiList[0].content == notification_content

    def test_bookingNotification(self):
        # Mock data
        payment = Payment(Decimal(100.0))
        screening = Screening(MockMovie('haha'), date.today(), datetime.now(), datetime.now() + timedelta(hours=2), CinemaHall('H1',100),[]) 
        seat = CinemaHallSeat("A", 1, False, Decimal(50.0))
        
        booking = Booking(self.customer, screening, True, 1, Decimal(50.0), payment)
        booking.addSeat(seat)



################################
class TestScreening:

    def setup_method(self, method):
        self.movie = MockMovie('Haha')
        self.screeningDate = date.today()
        self.startTime = datetime.now()
        self.endTime = self.startTime + timedelta(hours=2)
        self.hall = CinemaHall('H1', 20)  # Mocked CinemaHall instance.
        self.screening = Screening(self.movie, self.screeningDate, self.startTime, self.endTime, self.hall,[])
    
    def test_addSeat(self):
        seat = CinemaHallSeat("A", 1, False, Decimal(50.0))
        self.screening.addSeat(seat)

        assert len(self.screening.seats) == 1
        assert self.screening.seats[0] == seat

    def test_screeningAttributes(self):
        assert self.screening.movie == self.movie
        assert self.screening.screeningDate == self.screeningDate
        assert self.screening.startTime == self.startTime
        assert self.screening.endTime == self.endTime
        assert self.screening.status == True  # default status

    def test_setScreeningStatus(self):
        self.screening.status = False
        assert self.screening.status == False


class TestCinemaHallSeat:

    def setup_method(self):
        self.seat = CinemaHallSeat("B", 2, False, Decimal(60.0))

    def test_seatAttributes(self):
        assert self.seat.col == "B"
        assert self.seat.row == 2
        assert self.seat.isReserved == False
        assert self.seat.seatPrice == Decimal(60.0)

    def test_reserveSeat(self):
        self.seat.isReserved = True
        assert self.seat.isReserved == True

    def test_setUserID(self):
        user_id = "test_user"
        self.seat.userID = user_id
        assert self.seat.userID == user_id