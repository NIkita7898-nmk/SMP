from datetime import datetime
from django.db import models

from constant import PAYMENT_STATUS, PAYMENT_METHOD
from user.models import CustomUser

class Movie(models.Model):
    title = models.CharField(max_length=50)
    duration = models.IntegerField()
    rating = models.FloatField()
    release_date = models.DateField()
    description = models.TextField()


class Theaters(models.Model):
    name = models.CharField(max_length=60)
    location = models.CharField(max_length=255)
    number_of_screens = models.IntegerField()


class Screen(models.Model):
    screen_no = models.IntegerField()
    theater = models.ForeignKey(Theaters, on_delete=models.CASCADE)
    total_seats = models.IntegerField()


class ShowTimes(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater_id = models.ForeignKey(Theaters, on_delete=models.CASCADE)
    screen_id = models.ForeignKey(Screen, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    price = models.IntegerField()


class Seats(models.Model):
    screen_id = models.ForeignKey(Screen, on_delete=models.CASCADE)
    seat_number = models.IntegerField()


class Bookings(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    showtime_id = models.ForeignKey(ShowTimes, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=datetime.now)
    total_price = models.FloatField()
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='PENDING',
    )


class BookedSeats(models.Model):
    booking_id = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    seat_id = models.ForeignKey(Seats, on_delete=models.CASCADE)


class Payment(models.Model):
    booking_id = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD,
        default='COD',
    )
    payment_date = models.DateField()
