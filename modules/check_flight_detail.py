# check_flight_details.py

from .flight_ticket import FlightTicket  # Import FlightTicket class from booking_process.py


class FlightDetailsChecker:
    def __init__(self, booking_number):
        self.booking_number = booking_number
        self.flight_ticket = None

    def get_flight_details(self):
        # Assuming there's a method in FlightTicket to retrieve flight details by booking number
        self.flight_ticket = FlightTicket.get_flight_details_by_booking_number(self.booking_number)
        return self.flight_ticket

    def print_full_details(self):
        if self.flight_ticket:
            self.flight_ticket.print_details()
        else:
            print("Flight details not found.")


# Example usage
def main():
    booking_number = 1234  # Replace with actual booking number
    checker = FlightDetailsChecker(booking_number)

    flight_details = checker.get_flight_details()

    if flight_details:
        checker.print_full_details()
    else:
        print("No flight details found for this booking number.")


if __name__ == "__main__":
    main()
