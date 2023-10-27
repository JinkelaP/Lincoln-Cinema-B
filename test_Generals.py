from Generals import Guest, Customer, Admin, FrontDeskStaff, Movie, Screening, Booking, Notification, CinemaHall, CinemaHallSeat, Payment, Coupon, CreditCard, DebitCard, Cash
from decimal import Decimal
from datetime import date, datetime, timedelta
from typing import Union

import pytest

movies = [
    Movie("Inception", "Dream inside a dream", 150, "English", datetime.now() - timedelta(days=365), "USA", "Action"),
    Movie("Tenet", "Time inversion", 150, "English", datetime.now(), "USA", "Sci-Fi"),
    Movie("Intouchables", "Based on a true story", 112, "French", datetime.now() - timedelta(days=2000), "France", "Drama"),
]

testGuest = Guest()
testCustomer = Customer('Sam', '1 Queens St', '233@gmail.com', '0220220222','guestTest', 'guestTestP')


class TestGeneral:
    def setup_method(self):
        self.general = Guest()

    def test_search_movie_title_lang_genre(self):
        result = self.general.searchMovieTitleLangGenre("Inception", movies)
        assert len(result) == 1
        assert result[0].title == "Inception"

        # test if not existing
        result = self.general.searchMovieTitleLangGenre("NotExistingTitle", movies)
        assert len(result) == 0

    def test_search_movie_date(self):
        result = self.general.searchMovieDate(datetime.now() - timedelta(days=1000), movies)
        assert len(result) == 2

        # test order
        assert result[0].title == "Intouchables"
        assert result[1].title == "Inception"

    def test_view_movie_details(self):
        movie = movies[0]
        result = self.general.viewMovieDetails(movie)
        assert result['title'] == "Inception"
        assert result['language'] == "English"

class TestGuest:
    def setup_method(self):
        self.guest = Guest()

    def test_register(self):
        name = "John Doe"
        address = "123 Main St"
        email = "johndoe@example.com"
        phone = "123-456-7890"
        username = "johnD123"
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
            "John Doe",
            "123 Main St",
            "johndoe@example.com",
            "123-456-7890",
            "johnD123",
            "securepassword"
        )

    def test_initialization(self):
        assert self.admin.name == "John Doe"
        assert self.admin.address == "123 Main St"
        assert self.admin.email == "johndoe@example.com"
        assert self.admin.phone == "123-456-7890"
        assert self.admin.username == "johnD123"
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
        self.user = Admin(
            "John Doe",
            "123 Main St",
            "johndoe@example.com",
            "123-456-7890",
            "johnD123",
            "securepassword"
        )
        self.mock_movie = MockMovie('Haha')
        self.mock_screening = Screening(self.mock_movie, date.today(), datetime.now(), datetime.now() + timedelta(hours=2), None)
        self.mock_payment = Payment(Decimal(20.0))
        self.mock_seat1 = CinemaHallSeat("A", 1, False, Decimal(10.0))
        self.mock_seat2 = CinemaHallSeat("A", 2, False, Decimal(10.0))
        self.mock_screening.addSeat(self.mock_seat1)
        self.mock_screening.addSeat(self.mock_seat2)

    def test_makeBooking(self):
        booking = self.user.makeBooking(self.user, self.mock_screening, 2, Decimal(20.0), self.mock_payment)
        assert isinstance(booking, Booking)
        assert booking.customer == self.user
        assert booking.screening == self.mock_screening
        assert booking.numberOfSeats == 2
        assert booking.orderTotal == Decimal(20.0)
        assert booking.paymentDetail == self.mock_payment
        assert booking.status
        # Assert that seats are reserved
        assert self.mock_seat1.isReserved
        assert self.mock_seat2.isReserved

    def test_cancelBooking(self):
        booking = self.user.makeBooking(self.user, self.mock_screening, 2, Decimal(20.0), self.mock_payment)
        assert booking.status
        self.user.cancelBooking(booking)
        assert not booking.status
        # Assert that seats reservation is cancelled
        assert not self.mock_seat1.isReserved
        assert not self.mock_seat2.isReserved


#######################################################
class TestAdmin:
    def setup_method(self):
        self.admin = Admin(
            "John Doe",
            "123 Main St",
            "johndoe@example.com",
            "123-456-7890",
            "johnD123",
            "securepassword"
        )
        self.all_movies = []
        self.all_screenings = []

    def test_addMovie(self):
        movie = self.admin.addMovie("Inception", "Description", 120, "English", date(2010, 7, 16), "USA", "Sci-Fi", self.all_movies)
        assert movie in self.all_movies
        assert movie.title == "Inception"

    def test_addScreening(self):
        movie = MockMovie("Inception")
        screening = self.admin.addScreening(movie, date.today(), datetime.now(), datetime.now() + timedelta(hours=2), None, None, self.all_screenings)
        assert screening in self.all_screenings
        assert screening.movie == movie

    def test_cancelMovie(self):
        movie = MockMovie("Inception")
        self.all_movies.append(movie)
        assert movie.status
        self.admin.cancelMovie(movie)
        assert not movie.status

    def test_cancelScreening(self):
        movie = MockMovie("Inception")
        screening = Screening(movie, date.today(), datetime.now(), datetime.now() + timedelta(hours=2), None)
        self.all_screenings.append(screening)
        assert screening.status
        self.admin.cancelScreening(screening)
        assert not screening.status

#########################
class TestCustomer:

    def setup_method(self):
        self.customer = Customer("John Doe", "123 Main St", "johndoe@example.com", "123-456-7890", "johndoe", "password")
    
    def test_add_booking(self):
        # Mock data
        payment = Payment(Decimal(100.0))  # You might need to mock the Payment class as well.
        screening = Screening(Movie(), date.today(), datetime.now(), datetime.now() + timedelta(hours=2), CinemaHall()) 
        seat = CinemaHallSeat("A", 1, False, Decimal(50.0))
        
        booking = Booking(self.customer, screening, True, 1, Decimal(50.0), payment)
        booking.addSeat(seat)
        
        self.customer.addBookings(booking)
        
        assert len(self.customer.bookingList) == 1
        assert self.customer.bookingList[0].screening == screening
        assert self.customer.bookingList[0].seats[0] == seat

    def test_add_notification(self):
        # Mock data
        notification_content = "Your booking has been confirmed!"
        noti = Notification(self.customer, notification_content)

        self.customer.addNoti(noti)

        assert len(self.customer.notiList) == 1
        assert self.customer.notiList[0].content == notification_content

    def test_booking_notification(self):
        # Mock data
        payment = Payment(Decimal(100.0))
        screening = Screening(Movie(), date.today(), datetime.now(), datetime.now() + timedelta(hours=2), CinemaHall()) 
        seat = CinemaHallSeat("A", 1, False, Decimal(50.0))
        
        booking = Booking(self.customer, screening, True, 1, Decimal(50.0), payment)
        booking.addSeat(seat)
        booking.sendNotification()

        assert len(self.customer.notiList) == 1
        assert "confirmed" in self.customer.notiList[0].content


################################
class TestScreening:

    def setup_method(self, method):
        """Setup method that runs before each test"""
        self.movie = MockMovie('Haha')
        self.screeningDate = date.today()
        self.startTime = datetime.now()
        self.endTime = self.startTime + timedelta(hours=2)
        self.hall = CinemaHall('H1', 20)  # Mocked CinemaHall instance.
        self.screening = Screening(self.movie, self.screeningDate, self.startTime, self.endTime, self.hall)
    
    def test_add_seat(self):
        seat = CinemaHallSeat("A", 1, False, Decimal(50.0))
        self.screening.addSeat(seat)

        assert len(self.screening.seats) == 1
        assert self.screening.seats[0] == seat

    def test_screening_attributes(self):
        assert self.screening.movie == self.movie
        assert self.screening.screeningDate == self.screeningDate
        assert self.screening.startTime == self.startTime
        assert self.screening.endTime == self.endTime
        assert self.screening.status == True  # default status

    def test_set_screening_status(self):
        self.screening.status = False
        assert self.screening.status == False


class TestCinemaHallSeat:

    def setup_method(self, method):
        """Setup method that runs before each test"""
        self.seat = CinemaHallSeat("B", 2, False, Decimal(60.0))

    def test_seat_attributes(self):
        assert self.seat.col == "B"
        assert self.seat.row == 2
        assert self.seat.isReserved == False
        assert self.seat.seatPrice == Decimal(60.0)

    def test_reserve_seat(self):
        self.seat.isReserved = True
        assert self.seat.isReserved == True

    def test_set_user_id(self):
        user_id = "test_user"
        self.seat.userID = user_id
        assert self.seat.userID == user_id