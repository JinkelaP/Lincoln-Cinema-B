from Generals import Guest, Customer, Admin, FrontDeskStaff, Movie, Screening, Booking, Notification, CinemaHall, CinemaHallSeat, Payment, Coupon, CreditCard, DebitCard, Cash
from decimal import Decimal
from datetime import date, datetime, timedelta
from typing import Union

# movies = [
#     Movie("LincolnUniMovie", "Academic Film Assignment", 150, "English", datetime.now() - timedelta(days=365), "USA", "Action"),
#     Movie("WigramFight", "Lifestyle in Wigram but abnormal", 150, "English", datetime.now(), "USA", "Sci-Fi"),
#     Movie("HAHAHAHAHHAHAHA", "Documentary internet meme", 112, "French", datetime.now() - timedelta(days=2000), "France", "Drama"),
# ]

# general = FrontDeskStaff()
# # result = general.searchMovieDate(datetime.now() - timedelta(days=1000), movies)
# # print(result)
# # class MovieT:
# #     def __init__(self, title, releaseDate):
# #         self.title = title
# #         self.releaseDate = releaseDate

# # movie1 = MovieT("A", datetime(2022, 10, 28, 17, 35, 39, 181465))
# # movie2 = MovieT("B", datetime(2021, 1, 1, 12, 0, 0, 0))
# # movies = [movie1, movie2]

# # print(movies.sort(key=lambda movie: movie.releaseDate))

# booking = self.user.makeBooking(self.user, self.mock_screening, 2, Decimal(20.0), self.mock_payment)
# booking.addSeat(self.mock_seat1)
# booking.addSeat(self.mock_seat2)
# booking.status
# self.user.cancelBooking(booking)
# booking.status
# class MockMovie:
#     def __init__(self, title):
#         self.title = title
#         self.status = True

# class TestUserBooking:

#     def setup_method(self):
#         self.user = Customer(
#             "John Biden",
#             "12345 Main South Rd",
#             "johnthepresident@gmail.com",
#             "0220220222",
#             "johnbiden",
#             "securepassword"
#         )
#         self.mock_movie = MockMovie('Haha')
#         self.mock_screening = Screening(self.mock_movie, date.today(), datetime.now(), datetime.now() + timedelta(hours=2), None,[])
#         self.mock_payment = Payment(Decimal(20.0))
#         self.mock_seat1 = CinemaHallSeat("A", 1, False, Decimal(10.0))
#         self.mock_seat2 = CinemaHallSeat("A", 2, False, Decimal(10.0))
        

#     def test_makeBooking(self):
#         booking = self.user.makeBooking(self.user, self.mock_screening, 2, Decimal(20.0), self.mock_payment)
#         booking.addSeat(self.mock_seat1)
#         booking.addSeat(self.mock_seat2)
#         assert isinstance(booking, Booking)
#         assert booking.customer == self.user
#         assert booking.screening == self.mock_screening
#         assert booking.numberOfSeats == 2
#         assert booking.orderTotal == Decimal(20.0)
#         assert booking.paymentDetail == self.mock_payment
#         print(booking.status)


#     def test_cancelBooking(self):
#         booking = self.user.makeBooking(self.user, self.mock_screening, 2, Decimal(20.0), self.mock_payment)
#         booking.addSeat(self.mock_seat1)
#         booking.addSeat(self.mock_seat2)
#         print(booking.status)
#         self.user.cancelBooking(booking)
#         print(booking.status)

# eg = TestUserBooking()

# eg.setup_method()
# print('setup ok')
# eg.test_makeBooking()
# print('make booking ok')

Admin('Admin Zhu', '233Rd', 'e@e.com','233','admintest','233')

Customer()