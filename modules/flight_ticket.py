from datetime import date
import os
import random

# Remember to add "." before the python file name, when united with "chatbot.py"
import pandas as pd
from .person import Person  # Import the Person class from person


class FlightTicket:
    def __init__(self, flight_database):
        self.booking_number = None
        self.flightID = None
        self.destination = None
        self.departure = None
        self.list_of_passengers = []  # List of Person objects
        self.seat_numbers = []  # List of strings corresponding to passengers
        self.return_ticket = False
        self.departure_date = None  # datetime.date object
        self.return_date = None
        self.flight_time = None  # New attribute
        self.planeID = None  # New attribute
        self.ticket_class = None  # e.g., 'Economy' for economy, 'Business' for business
        self.choose_seat = False  # Future implementation
        self.price = None
        self.total_price = None
        self.load_database(flight_database) # "Flight-DB.csv"
        self.generate_booking_number()


    def load_database(self, file_path):
        """Loads the flight database into memory."""
        try:
            self.flight_data = pd.read_csv(file_path)
        except FileNotFoundError:
            print("Error: Flight database file not found.")
            #self.flight_data = pd.DataFrame() # Empty DataFrame if file not found

    def update_flight_details(self):
        """Updates flight details based on the current attributes."""
        if self.destination and self.departure and self.ticket_class:
            # Filter the database for the matching flight
            matching_flight = self.flight_data[
                (self.flight_data['Destination'] == self.destination) &
                (self.flight_data['Departure'] == self.departure) &
                (self.flight_data['Class'] == self.ticket_class)
                ]
            if not matching_flight.empty:
                # Assume there's only one match due to unique combination
                flight_row = matching_flight.iloc[0]
                self.flightID = flight_row['Flight ID']
                self.flight_time = flight_row['Flight Time']
                self.planeID = flight_row['Plane ID']
                self.price = flight_row['Return Price'] if self.return_ticket else flight_row['Price']
            else:
                print("Error: No matching flight found.")

    def calculate_total_price(self):
        self.total_price = self.price * len(self.list_of_passengers)

    # Print the SIMPLE details of the flight ticket
    def print_simple_details(self):
        """Prints simple details of the flight ticket."""
        print(f"Flight Ticket Details: Flight ID: {self.flightID}, Destination: {self.destination}, Departure: {self.departure}, Class: {self.ticket_class}, Return Ticket: {self.return_ticket}, Departure Date: {self.departure_date}, Return Date: {self.return_date}")

    # Print the details WITHOUT price of the flight ticket
    def print_details_without_price(self):
        """Prints details of the flight ticket, WITHOUT price."""
        print("\nFlight Ticket Details:")
        print(f"Booking Number: {self.booking_number}")
        print(f"Flight ID: {self.flightID}")
        print(f"Destination: {self.destination}")
        print(f"Departure: {self.departure}")
        print(f"Flight Time: {self.flight_time}")
        print(f"Plane ID: {self.planeID}")
        print(f"Class: {self.ticket_class}")
        print(f"Return Ticket: {'Yes' if self.return_ticket else 'No'}")
        print(f"Departure Date: {self.departure_date}")
        if self.return_ticket:
            print(f"Return Date: {self.return_date}")
        #print(f"Seat Numbers: {', '.join(self.seat_numbers) if self.seat_numbers else 'Not assigned yet'}")
        print("Passengers:")
        if self.list_of_passengers:
            for i, passenger in enumerate(self.list_of_passengers, start=1):
                print(f"  Passenger {i}: {passenger.full_name}, DOB: {passenger.dob}")
        else:
            print("  No passengers added yet.")
        print()

    # Print the FULL details of the flight ticket
    def print_details(self):
        """Prints all details of the flight ticket."""
        print("\nFlight Ticket Details:")
        print(f"Booking Number: {self.booking_number}")
        print(f"Flight ID: {self.flightID}")
        print(f"Destination: {self.destination}")
        print(f"Departure: {self.departure}")
        print(f"Flight Time: {self.flight_time}")
        print(f"Plane ID: {self.planeID}")
        print(f"Class: {self.ticket_class}")
        print(f"Return Ticket: {'Yes' if self.return_ticket else 'No'}")
        print(f"Departure Date: {self.departure_date}")
        if self.return_ticket:
            print(f"Return Date: {self.return_date}")
        #print(f"Seat Numbers: {', '.join(self.seat_numbers) if self.seat_numbers else 'Not assigned yet'}")
        print("Passengers:")
        if self.list_of_passengers:
            for i, passenger in enumerate(self.list_of_passengers, start=1):
                print(f"  Passenger {i}: {passenger.full_name}, DOB: {passenger.dob}")
        else:
            print("  No passengers added yet.")
        print(f"Price: ${self.price if self.price is not None else 'Not calculated yet'}")
        print()

    def generate_booking_number(self):
        self.booking_number = random.randint(1001, 9999)

    # Getters
    def get_booking_number(self):
        return self.booking_number

    def get_flightID(self):
        return self.flightID

    def get_destination(self):
        return self.destination

    def get_departure(self):
        return self.departure

    def get_list_of_passengers(self):
        return [person.full_name for person in self.list_of_passengers]

    def get_seat_numbers(self):
        return self.seat_numbers

    def get_return_ticket(self):
        return self.return_ticket

    def get_departure_date(self):
        return self.departure_date

    def get_return_date(self):
        return self.return_date

    def get_flight_time(self):
        return self.flight_time  # Getter for flight_time

    def get_planeID(self):
        return self.planeID  # Getter for planeID

    def get_ticket_class(self):
        return self.ticket_class

    def get_choose_seat(self):
        return self.choose_seat

    def get_price(self):
        return self.price

    # Setters
    def set_booking_number(self, booking_number):
        self.booking_number = booking_number

    def set_flightID(self, flightID):
        self.flightID = flightID

    def set_destination(self, destination):
        self.destination = destination
        self.update_flight_details()

    def set_departure(self, departure):
        self.departure = departure
        self.update_flight_details()

    def add_passenger(self, passenger, seat_number=None):
        if isinstance(passenger, Person):
            self.list_of_passengers.append(passenger)
            self.seat_numbers.append(seat_number)

    def remove_passenger(self, passenger):
        if passenger in self.list_of_passengers:
            index = self.list_of_passengers.index(passenger)
            self.list_of_passengers.pop(index)
            self.seat_numbers.pop(index)

    def set_return_ticket(self, return_ticket):
        self.return_ticket = return_ticket
        self.update_flight_details()

    def set_departure_date(self, departure_date):
        self.departure_date = departure_date

    def set_return_date(self, return_date):
        self.return_date = return_date

    def set_flight_time(self, flight_time):
        self.flight_time = flight_time  # Setter for flight_time

    def set_planeID(self, planeID):
        self.planeID = planeID  # Setter for planeID

    def set_ticket_class(self, ticket_class):
        self.ticket_class = ticket_class
        self.update_flight_details()

    def set_choose_seat(self, choose_seat):
        self.choose_seat = choose_seat

    def set_price(self, price):
        self.price = price

    def remove_all_passengers(self):
        self.list_of_passengers = []
        self.seat_numbers = []

