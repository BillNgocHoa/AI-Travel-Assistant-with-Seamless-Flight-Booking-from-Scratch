from flight_ticket import FlightTicket


def test_update_flight_details():
    # Create a FlightTicket object
    flight_ticket = FlightTicket()

    # Load the flight database
    #flight_ticket.load_database("Flight-DB.csv")

    # Set the attributes
    flight_ticket.set_departure("France")
    flight_ticket.set_destination("London")
    flight_ticket.set_ticket_class("Business")
    flight_ticket.set_return_ticket(True)

    # Update flight details
    # flight_ticket.update_flight_details()

    # Print the updated attributes to verify
    print(f"Flight ID: {flight_ticket.flightID}")
    print(f"Flight Time: {flight_ticket.flight_time}")
    print(f"Plane ID: {flight_ticket.planeID}")
    print(f"Price: {flight_ticket.price}")

if __name__ == "__main__":
    # Run the test
    test_update_flight_details()