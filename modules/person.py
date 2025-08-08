from datetime import date
from datetime import datetime


class Person:
    def __init__(self):
        self.name = None
        self.full_name = None
        self.dob = None
        self.age = None
        self.phone_num = None
        self.following_passengers = []  # List of Person objects
        self.flight_booking_num = None
        self.hotel_booking_num = None

    # Getters
    def get_name(self):
        return self.name

    def get_full_name(self):
        return self.full_name

    def get_dob(self):
        return self.dob

    def get_age(self):
        return self.age

    def get_phone_num(self):
        return self.phone_num

    def get_following_passengers(self):
        return self.following_passengers

    def get_flight_booking_num(self):
        return self.flight_booking_num

    def get_hotel_booking_num(self):
        return self.hotel_booking_num

    # Setters
    def set_name(self, name):
        self.name = name

    def set_full_name(self, full_name):
        self.full_name = full_name

    def set_dob(self, dob):
        self.dob = dob
        self.calculate_age()  # Automatically update age when DOB is set

    def set_phone_num(self, phone_num):
        self.phone_num = phone_num

    def add_following_passenger(self, passenger):
        if isinstance(passenger, Person):
            self.following_passengers.append(passenger)

    def remove_following_passenger(self, passenger):
        if passenger in self.following_passengers:
            self.following_passengers.remove(passenger)

    def set_flight_booking_num(self, booking_num):
        self.flight_booking_num = booking_num

    def set_hotel_booking_num(self, booking_num):
        self.hotel_booking_num = booking_num

    # Utility methods
    def calculate_age(self):
        if self.dob:
            today = date.today()
            self.age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return self.age

    def __str__(self):
        return f"{self.full_name}, DOB: {self.dob}, Age: {self.age}, Phone: {self.phone_num}"
