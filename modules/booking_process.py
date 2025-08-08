import time
from datetime import datetime

from nltk import download_gui
from numpy.ma.core import append

# Remember to add "." before the python file name, when united with "chatbot.py"
from .person import Person
from .flight_ticket import FlightTicket
from .text_preprocessor import TextPreprocessor


class BookingProcess:
    def __init__(self, flight_database, user_general):
        self.user = user_general
        #self.user_name = self.user.get_name()
        self.stages = []  # Stack to track process stages
        self.current_stage = None
        self.in_booking_process = False
        self.booking_manager = BookingDetailsManager(flight_database)
        self.negativity_handler = NegativityHandler()
        self.text_preprocessor = TextPreprocessor()
        self.special_keywords = ["cancel", "don't", "stop", "restart", "back", "exit", "quit", "not", "false", "what can you do"]  # Example special keywords

    def check_special_keywords(self, user_input):
        """Detect and handle special keywords."""
        user_input_lower = user_input.lower()
        if any(keyword in user_input_lower for keyword in self.special_keywords):
            if "cancel" in user_input_lower or "quit" in user_input_lower or "exit" in user_input_lower or "stop" in user_input_lower or "what can you do" in user_input_lower:
                self.handle_cancel()
            elif "restart" in user_input_lower:
                self.handle_restart()
            elif "back" in user_input_lower:
                self.handle_back_to_previous_stage()
            elif any(keyword in user_input_lower for keyword in ["no", "don't", "not", "false", "change", "wrong"]):
                self.handle_back()
            return True
        return False

    def start_booking(self):
        """Starts the booking process."""
        self.in_booking_process = True
        self.stages.append("Starting the Conversation")
        self.current_stage = "Starting the Conversation"
        print(f"Chatbot: I'm ready to help you book your flight, {self.user.get_name()}! 😊 Let's get started.")
        print("Chatbot: I'll guide you through the process step by step.\n"
              "         Step 1: Gathering Flight Information \n"
              "         Step 2: Filling Personal Details \n"
              "         Step 3: Confirming Booking Details \n"
              "         Step 4: Processing Payment \n")

        print("Quick note: \n"
              "         You can type 'back' to go BACK to the previous step.\n"
              "         You can type 'restart' to RESTART the booking process again.\n"
              "         You can type 'cancel' to CANCEL the booking process at any time.\n")

        print("Chatbot: Our airline provides service to 4 countries with flights to:"
              "\n\t\t\t England \n\t\t\t Singapore \n\t\t\t France \n\t\t\t Spain")
        print()
        print("Chatbot: Shall we begin? 🚀")
        self.next_stage()

    def next_stage(self):
        """Moves to the next stage of the booking process."""
        if self.current_stage == "Starting the Conversation":
            self.current_stage = "Gathering Flight Information"
            self.stages.append(self.current_stage)
            self.gather_flight_information()
        elif self.current_stage == "Gathering Flight Information":
            self.current_stage = "Asking for Personal Information"
            self.stages.append(self.current_stage)
            self.ask_personal_information()
        elif self.current_stage == "Asking for Personal Information":
            self.current_stage = "Confirming Booking Details"
            self.stages.append(self.current_stage)
            self.confirm_booking_details()
        elif self.current_stage == "Confirming Booking Details":
            self.current_stage = "Processing Payment"
            self.stages.append(self.current_stage)
            self.process_payment()
        else:
            print("Chatbot: Booking process completed!")
            self.complete_booking()
            #self.booking_manager.confirm_details_before_payment()


# Small functions to handle specific stages of the booking process
    def handle_cancel(self):
        """Handles cancellation of the booking process."""
        self.in_booking_process = False
        print("Chatbot: Your booking process has been canceled.")
        return None

    def handle_restart(self):
        """Handles restarting the current stage."""
        print("Chatbot: Restarting the booking process. Back to the very beginning!")
        # self.stages.pop()  # Remove the current stage
        # self.next_stage()  # Restart the stage
        self.booking_manager.remove_all_passengers()  # Remove all passengers
        self.stages.clear() # Clear all stages in the stack
        self.start_booking()

    def handle_back(self):
        """Handles going back to the previous stage."""
        if len(self.stages) > 1:
            self.stages.pop()
            self.current_stage = self.stages[-1]
            print(f"Chatbot: I'm sorry to here that 😢. Going back to beginning the stage.")
            self.next_stage()
        else:
            print("Chatbot: You're at the beginning of the booking process and cannot go back further.")

    def handle_back_to_previous_stage(self):
        """Handles going back to the previous stage."""
        if len(self.stages) > 1:
            self.stages.pop()
            if self.current_stage == "Gathering Flight Information":
                self.current_stage = "Starting the Conversation"
                print("Chatbot: Going back to the beginning of the booking process.")
            else:
                self.current_stage = self.stages[-2] # Go back to the previous stage
                print(f"Chatbot: Going back to the previous step: {self.stages[+1]}.")
            self.next_stage()
        else:
            print("Chatbot: You're at the beginning of the booking process and cannot go back further.")

    def get_user_input(self, prompt):
        """Gets user input and checks for special keywords."""
        user_input = input(prompt)
        if self.check_special_keywords(user_input):
            return None  # Interrupt the process if a special keyword is detected
        return user_input


    def detect_location(self, location_input):
        # Detect location
        detected_locations = self.text_preprocessor.detect_location(location_input)
        if detected_locations:
            location = detected_locations[0]  # Choose the first detected location
            if location not in ["England", "Singapore", "France", "Spain"]:
                print(f"Chatbot: I'm sorry, we only support flights to England, Singapore, France, and Spain. Could you please specify again?")
                return self.detect_location(self.get_user_input("User: "))
            return location
        else:
            print("Chatbot: I couldn't detect the location. Could you please specify the location clearly?")
            #return self.gather_flight_information()  # Ask again if no location is detected
            return self.detect_location(self.get_user_input("User: "))

    def get_valid_date(self, prompt, place=None):
        while True:
            date_input = self.get_user_input(prompt)
            if date_input is None:
                return
            try:
                date = datetime.strptime(date_input, "%d/%m/%Y").date()
                # check if the date is in the future
                if date < datetime.now().date():
                    print(f"Chatbot: I'm sorry, the {place} date must be in the future. Please enter again.")
                    continue # Ask for the date again
                else:
                    if place:
                        print(f"Chatbot: {place} date: ", date)
                    return date
            except ValueError:
                print("Chatbot: Sorry I couldn't recognise the date format! Please enter in DD/MM/YYYY format.")

    def get_valid_dob(self, prompt):
        while True:
            dob_input = self.get_user_input(prompt)
            if dob_input is None:
                return
            try:
                dob = datetime.strptime(dob_input, "%d/%m/%Y").date()
                # check if the date is in the future
                if dob > datetime.now().date():
                    print("Chatbot: I'm sorry, the date of birth must be in the past. Please enter again.")
                    continue # Ask for the date again
                else:
                    print("Chatbot: Date of Birth: ", dob)
                    return dob
            except ValueError:
                print("Chatbot: Sorry I couldn't recognise the date format! Please enter the date of birth in DD/MM/YYYY format.")
                continue



# The Booking Process stages start here:

    def gather_flight_information(self):
        """Stage to gather flight details from the user."""
        print(f"Chatbot: First of all, could you please tell me which country you are flying to, {self.user.get_name()}?")  # Suggest some destinations
        destination_input = self.get_user_input("User: ")
        if destination_input is None:
            return  # Stop further processing if a special keyword is detected
        destination = self.detect_location(destination_input)

        print(f"Chatbot: Got it - {destination} it is! And which country will you be flying from?") # Suggest some departure locations
        departure_input = self.get_user_input("User: ")
        if departure_input is None:
            return
        departure = self.detect_location(departure_input)

        print(f"Chatbot: Nice, {self.user.get_name()}. Will this be a one-way trip or a return ticket?")
        ticket_type = self.get_user_input("User: ")
        if ticket_type is None:
            return # Stop further processing if a special keyword is detected
        if "return" in ticket_type.lower():
            ticket_type = "return"
        elif "one" in ticket_type.lower():
            ticket_type = "one-way"

        print(f"Chatbot: Gotcha, that's a {ticket_type} ticket. What’s the departure date? (DD/MM/YYYY)")
        departure_date = self.get_valid_date("User: ", "Departure")
        if departure_date is None:
            return

        # Check if return ticket -> Ask for return date
        if "return" in ticket_type.lower():
            print("Chatbot: Gotcha! And what’s your return date? (DD/MM/YYYY)")
            return_date = self.get_valid_date("User: ", "Return")
            while return_date < departure_date:
                print("Chatbot: I'm sorry, the return date must be after the departure date. Please enter again.")
                return_date = self.get_valid_date("User: ", "Return")
            if return_date is None:
                return
        elif "one" in ticket_type.lower():
            return_date = None
        else:
            print("Chatbot: I'm sorry, I didn't catch that. Is this a one-way or return ticket?")
            self.gather_flight_information()
            return # Exit the function to prevent moving to the next stage if the input is invalid or unclear

        print(f"Chatbot: What do you prefer, {self.user.get_name()}? Business class or Economy class?")
        ticket_class = self.get_user_input("User: ")
        if ticket_class is None:
            return
        if "business" in ticket_class.lower():
            ticket_class = "Business"
            print(f"Chatbot: Perfect choice! You will have a most comfortable flight ever 💖.")
        else:
            ticket_class = "Economy"
            print(f"Chatbot: Smart choice! Save money for the food, huh? 🤤.")

        # Store details in BookingDetailsManager
        self.booking_manager.update_flight_details(
            destination=destination,
            departure=departure,
            ticket_type=ticket_type,
            departure_date=departure_date,
            return_date=return_date,
            ticket_class=ticket_class
        )

        print()
        print("Chatbot: Let's moving to the 2nd step 🚀: Gathering personal information.")
        self.next_stage()


    def ask_personal_information(self):
        """Stage to gather personal information."""
        print("Chatbot: Now, I need your details for the ticket.")
        print(f"Chatbot: What is your full name, {self.user.get_name()}?")
        full_name = self.get_user_input("User: ")
        if full_name is None:
            return

        print("Chatbot: And your date of birth? (DD/MM/YYYY) ")
        # Convert to datetime.date object
        dob_user_input = self.get_valid_dob("User: ")
        if dob_user_input is None:
            return
        dob = dob_user_input

        phone_number = self.get_user_input("Chatbot: Cool, and your phone number is? ")
        if phone_number is None:
            return

        print(f"Testing: {full_name}, {dob}, {phone_number}")  # Testing

        # Add the primary user as a passenger
        self.booking_manager.add_passenger(full_name, dob, phone_number)

        print("Chatbot: How many passengers, including yourself, will be traveling?")
        num_passengers = int(self.get_user_input("User: "))
        if num_passengers is None:
            return

        for i in range(2, num_passengers + 1):
            print(f"Chatbot: Could you please tell me about Passenger {i}?")
            print(f"Chatbot: What is the full name of Passenger {i}?")
            full_name = self.get_user_input("User: ")
            if full_name is None:
                return
            print(f"Chatbot: And the date of birth for Passenger {i}? (DD/MM/YYYY) ")
            #dob_user_input = self.get_user_input(f"Chatbot: Date of birth for Passenger {i}? (DD/MM/YYYY) ")
            dob_user_input = self.get_valid_dob("User: ")
            if dob_user_input is None:
                return
            dob = dob_user_input
            # Convert to datetime.date object
            # try:
            #     dob = datetime.strptime(dob_user_input, "%d/%m/%Y").date()
            #     print("Date of Birth:", dob)
            # except ValueError:
            #     print("Invalid date format! Please enter the date in DD/MM/YYYY format.")
            self.booking_manager.add_passenger(full_name, dob)

        print(f"Chatbot: Thanks, {self.user.get_name()}! All passenger details have been noted.\n")
        self.next_stage()

    def handle_interruption(self):
        """Handles user interruptions."""
        print("Chatbot: It seems like you want to stop or change something. Let me know how I can assist!")
        # Add logic to backtrack or update stages
        print("Chatbot: Would you like to go Back to previous step, Restart the booking process or Cancel it? (Please type 'back', 'restart', or 'cancel')")
        user_input = input("User: ").lower()
        if "restart" in user_input:
            # Delete the passenger details and flight ticket (if they exist)
            self.booking_manager.remove_all_passengers() # Remove all passengers
            # self.booking_manager.flight_ticket = None  # Remove flight ticket

            # Add logic to empty the stack, here.
            self.stages.clear()  # Clear all stages in the stack

            # self.stages.pop()  # Remove current stage -> Remove everything in stack
            # self.current_stage = "Starting the Conversation"  # Go back to very beginning
            # self.next_stage()  # Then next step -> means Restart
            self.start_booking()

        elif "back" in user_input:
            if len(self.stages) > 1:
                # Delete the passenger details, which is  (if they exist)
                self.booking_manager.remove_all_passengers() # Remove all passengers

                self.stages.pop()
                self.current_stage = self.stages[-2] # Go back to the previous stage
                self.next_stage()
            else:
                print("Chatbot: You're at the beginning of the booking process.")
        elif "cancel" in user_input:
            self.handle_cancel()
            print("Chatbot: Your booking process has been canceled.")
            #self.in_booking_process = False
        else:
            print("Chatbot: I didn't understand that. Let's try again.")
            self.handle_interruption()


    def confirm_booking_details(self):
        """Confirms the booking details with the user."""
        self.booking_manager.confirm_details_before_payment()
        print(f"Chatbot: Does everything look good to you, {self.user.get_name()}?")

        user_input = self.get_user_input("User: ")
        if user_input is None:
            return
        if self.negativity_handler.detect_negativity(user_input):
            self.handle_interruption()
        else:
            print("Chatbot: Great! (next step is Calculating the Price)")
            print()
            self.next_stage()

    ''' 
        Need to calculate the price based on the flight details and number of passengers.
        Then proceed to payment processing.
        
        print("Chatbot: Great! Let's go to the final step: Processing payment.")

    '''

    def check_payment_method(self, payment_method):
        if "credit" in payment_method.lower() or "card" in payment_method.lower():
            payment_method = "Credit Card"
            print("Chatbot: Great! You want to pay using Credit Card.")
        elif "paypal" in payment_method.lower():
            payment_method = "PayPal"
            print("Chatbot: Great! You want to pay using PayPal.")
        elif "apple" in payment_method.lower():
            payment_method = "Apple Pay"
            print("Chatbot: Great! You want to pay using Apple Pay.")
        else:
            print(f"Chatbot: I'm sorry {self.user.get_name()}, we only accept Credit Card, PayPal, or Apple Pay. Please choose one of these options.")
            payment_method = self.get_user_input("User: ")
            if payment_method is None:
                return
            return self.check_payment_method(payment_method)
        return payment_method

    def process_payment(self):
        """Handles the payment process."""
        print("Chatbot: Please wait one moment, while I calculate the cost...")

        time.sleep(3)  # Simulate calculating the price
        total_price = self.booking_manager.flight_ticket.price * len(self.booking_manager.passengers)
        #total_price = self.booking_manager.flight_ticket.calculate_total_price()
        print(f"Chatbot: The total cost for your flight is £{total_price}.")

        print("Chatbot: How would you like to pay for your ticket? We accept Credit Card, PayPal, or Apple Pay.")
        payment_method = self.get_user_input("User: ")
        if payment_method is None: # Check for special keywords
            return
        payment_method = self.check_payment_method(payment_method)
        print("Chatbot: We are now processing your payment. Please wait a moment...")
        # Add payment processing logic here

        time.sleep(5) # Wait 5 seconds to simulate payment processing
        print(f"Chatbot: Your payment has been successfully processed! Congratulations {self.user.get_name()}🎉")
        self.next_stage()


    def complete_booking(self):
        """Marks the booking process as completed."""
        self.in_booking_process = False
        self.booking_manager.confirm_details_after_payment()
        print("Chatbot: Your flight is officially booked! Thank you for choosing our service. 🛫")
        # print("Chatbot: Your flight is officially booked!\n"
        #       "         Please REMEMBER your BOOKING NUMBER. You can use it to check your Flight Details later\n\n"
        #       "         Thank you for choosing our service. Have a save flight! 🛫")
        print()


class BookingDetailsManager:
    def __init__(self, flight_database):
        self.flight_ticket = FlightTicket(flight_database)  # Initialize FlightTicket once booking starts
        self.passengers = [] # List of Person objects

    def update_flight_details(self, **kwargs):
        """Updates specific flight ticket details."""
        # Use setters or direct attribute updates
        if "destination" in kwargs:
            self.flight_ticket.set_destination(kwargs["destination"])
        if "departure" in kwargs:
            self.flight_ticket.set_departure(kwargs["departure"])
        if "ticket_type" in kwargs:
            self.flight_ticket.set_return_ticket(kwargs["ticket_type"].lower() == "return")
        if "departure_date" in kwargs:
            self.flight_ticket.set_departure_date(kwargs["departure_date"])
        if "return_date" in kwargs:
            self.flight_ticket.set_return_date(kwargs["return_date"])
        if "ticket_class" in kwargs:
            self.flight_ticket.set_ticket_class(kwargs["ticket_class"])
        # self.flight_ticket.print_simple_details()

    def add_passenger(self, full_name=None, dob=None, phone_number=None):
        """Adds a new passenger to the flight, with optional updates."""
        if full_name:  # Ensure at least full name is provided
            passenger = Person()  # Create a new Person object
            if full_name:
                passenger.set_full_name(full_name)
                passenger.set_name(full_name.split()[0])  # Set first name
            if dob:
                passenger.set_dob(dob)
            if phone_number:
                passenger.set_phone_num(phone_number)
            self.passengers.append(passenger)  # Add the passenger to the list
            if self.flight_ticket:
                self.flight_ticket.add_passenger(passenger)  # Link passenger to the flight ticket
        else:
            print("At least a full name or date of birth must be provided.")

    def remove_all_passengers(self):
        """Removes all passengers from the flight."""
        self.passengers.clear()
        if self.flight_ticket:
            self.flight_ticket.remove_all_passengers()

    def update_passenger_details(self, index, full_name=None, dob=None, phone_number=None):
        """Updates an existing passenger's details."""
        if 0 <= index < len(self.passengers):
            passenger = self.passengers[index]
            if full_name:
                passenger.full_name = full_name
                passenger.name = full_name.split()[0]  # Update first name
            '''Remember to check DOB format before updating (DD/MM/YYYY)'''
            if dob:
                passenger.dob = dob
            if phone_number:
                passenger.phone_num = phone_number
        else:
            print("Passenger index out of range.")

    def confirm_details_before_payment(self):
        """Prints a summary of the booking, BEFORE payment."""
        print("Chatbot: Here’s a summary of your booking so far:")
        if self.flight_ticket:
            self.flight_ticket.print_details_without_price()  # Print details without price

    def confirm_details_after_payment(self):
        """Prints a summary of the booking, AFTER payment."""
        print("Chatbot: Please find your flight details below:")
        if self.flight_ticket:
            self.flight_ticket.print_details() # Print full details with price


class NegativityHandler:
    def __init__(self):
        self.negative_words = ["no", "not", "back", "stop", "don't", "cancel", "change", "wrong", "false"]

    def detect_negativity(self, user_input):
        """Detects negative words in the user's input."""
        return any(word in user_input.lower() for word in self.negative_words)

    def handle_negativity(self):
        """Handles the detected negativity."""
        print("Chatbot: It seems like you want to change or stop something. Let me assist!")
        # Add further handling for backtracking or stage resetting


# Example Usage
# if __name__ == "__main__":
#     flight_database = "Flight-DB.csv"
#     process = BookingProcess(flight_database)
#     process.start_booking()
