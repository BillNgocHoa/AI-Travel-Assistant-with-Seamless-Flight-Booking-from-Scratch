import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .text_preprocessor import TextPreprocessor
from .person import Person

class IdentityManager:
    def __init__(self, dataset, user_general):
        # self.user_name = None
        self.user_attributes = {}  # Dictionary to store user attributes dynamically (e.g., {"name": "John"})
        self.text_processor = TextPreprocessor() # To process names
        self.user = user_general
        self.dataset = dataset
        # self.preprocessor = preprocessor
        self.vectorizer = TfidfVectorizer()
        self.X = self.vectorizer.fit_transform(self.dataset['Processed_User_Input'])

    def handle_identity(self, user_input, preprocessor):
        user_input_original = user_input
        user_input = user_input.lower()
        processed_input = preprocessor.preprocess_text_not_remove_stopwords(user_input)
        input_vector = self.vectorizer.transform([processed_input])
        similarities = cosine_similarity(input_vector, self.X)
        best_match_idx = similarities.argmax()
        #print(best_match_idx) # this is the index (the row number) of the best match

        if similarities[0, best_match_idx] > 0.3:  # A reasonable similarity threshold
            match = self.dataset.iloc[best_match_idx]
            required_tag = match['Required_Tag'].strip() if pd.notna(match['Required_Tag']) else ""
            #response = match['Answer']

            # Check if the response requires a specific attribute (e.g., name)
            if required_tag:
                # Check if the user's input is a question?
                if any(keyword in user_input for keyword in ["what", "who", "why", "how", "where", "when"]):
                    # If the attribute is missing, prompt the user to provide it
                    if required_tag not in self.user_attributes or not self.user_attributes[required_tag]: # If the attribute is missing or empty
                        print(f"Chatbot: I haven't known your {required_tag} yet. Please tell me.😊")
                        user_input_nested = input("User: ")
                        user_provided_value = self.detect_user_attribute(user_input_nested, required_tag)

                        # Update the attribute dynamically
                        self.update_attribute(required_tag, user_provided_value)
                        return match['Answer'].format(self.user_attributes[required_tag]) # Return the corresponding response with the attribute

                    # If the attribute is available, use it in the response
                    return match['Answer'].format(self.user_attributes[required_tag])

                # Update attribute Automatically (everytime user input is detected: My name is ...)
                user_provided_value = self.detect_user_attribute(user_input_original, required_tag)
                self.update_attribute(required_tag, user_provided_value)

                return match['Answer'].format(self.user_attributes[required_tag])

            # If no required attribute, return the response as the provided answer
            return match['Answer']

            # if required_tag:  # If an attribute is required (e.g., "name")
            #     if required_tag in self.attributes and self.attributes[required_tag]:
            #         # Replace '{}' with the attribute's value
            #         return response.format(self.attributes[required_tag])
            #     else:
            #         # Prompt the user to provide the required attribute
            #         return f"(Identity) I'm sorry, I don't know your {required_tag} yet. Please tell me."
            #
            # return response  # No attribute is required, just return the response
        return "(Identity) Sorry, I didn't recognise that. Could you please rephrase it?"

    """Updates a user attribute (require_tag) dynamically."""
    def update_attribute(self, required_tag, user_provided_value):
        # Get the last word as name and capitalize it
        self.user_attributes[required_tag] = user_provided_value
        if required_tag == "name":
            self.user.set_name(user_provided_value)
        # print("User-general name: ", self.user.get_name())

        # Testing purposes
        #print(f"Chatbot: Thank you! I've updated your {required_tag} to: {user_provided_value}.")

    def detect_user_attribute(self, user_input_original, required_tag):
        #print("User input: ", user_input_original)
        if required_tag == "age":
            detected_age = self.text_processor.detect_age(user_input_original)
            user_provided_value = detected_age if detected_age else "User - No Age"

        if required_tag == "name":
            if user_input_original == user_input_original.lower(): # if the user's input is in lowercase
                user_provided_value = user_input_original.strip().split()[-1].capitalize()  # can be replaced by the preprocessor (this old method only works for NAME)
            else:
                # if input is NOT in lowercase
                detected_names = self.text_processor.detect_name(user_input_original)  # [0] # if required_tag == "name" else None
                user_provided_value = detected_names[0] if detected_names else "User - No Name"
                if user_provided_value == "User - No Name":
                    print("Chatbot: Sorry, I didn't catch your name. Could you please capitalize your Name?")
                    user_input_nested = input("User: ")
                    user_provided_value = self.detect_user_attribute(user_input_nested, required_tag)
        return user_provided_value

        # if similarities[0, best_match_idx] > 0.3:
        #     # if the column 'Required_Tag' in dataset contains "name",
        #     # then the bot will check if the user's name is not empty.
        #     if "name" in self.dataset.iloc[best_match_idx]['Required_Tag']:
        #         # Case 1: User introduces their name FIRST
        #         if self.user_name:
        #             # if the user's name is not empty, the bot will return the answer with user's name
        #             response = self.dataset.iloc[best_match_idx]['Answer']
        #             return response.format(self.user_name) if '{}' in response else response  # return this if the answer contains '{}'
        #         # Case 2: User asks "What is my name?" & they haven't introduced yet
        #         else:
        #             # if the user's name is empty, the bot will ask for user's name
        #             return "(Identity) I'm sorry, I don't know your name yet. What is your name?"
        #     else:
        #         return self.dataset.iloc[best_match_idx]['Answer']
        #
        # return "(Identity) I'm not sure how to respond to that."

        # user_input = user_input.lower()
        # # Case 1: User introduces their name FIRST
        # if "my name is" in user_input:
        #     self.user_name = user_input.split("my name is")[-1].strip().capitalize()
        #     return f"Nice to meet you, {self.user_name}!"
        # elif "call me" in user_input:
        #     self.user_name = user_input.split("call me")[-1].strip().capitalize()
        #     return f"Okay, I'll call you {self.user_name}!"
        #
        # # Case 2: User asks "What is my name?" & even they haven't introduced yet
        # elif "what is my name" in user_input:
        #     if self.user_name:
        #         return f"Your name is {self.user_name}."
        #     else:
        #         return "I don't know your name yet. What is your name?"
        # return "(Identity) I can remember your name if you tell me!"  # return this if input is not contain "What is my name"

    def get_user_attribute(self, attribute):
        return self.user_attributes.get(attribute, None)  # Return None if the attribute is not found

