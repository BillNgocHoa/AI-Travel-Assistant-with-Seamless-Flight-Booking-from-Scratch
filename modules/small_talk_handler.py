from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
'''
Have to transform to use dataset and preprocessor to do matching.
This module contains the SmallTalkHandler class, which is responsible for handling small talk interactions.
'''

class SmallTalkHandler:
    def __init__(self, dataset):
        self.dataset = dataset
        #self.preprocessor = preprocessor
        self.vectorizer = TfidfVectorizer()
        self.X = self.vectorizer.fit_transform(self.dataset['Processed_User_Input'])

    def find_answer(self, user_input, preprocessor):
        processed_input = preprocessor.preprocess_text_not_remove_stopwords(user_input)
        input_vector = self.vectorizer.transform([processed_input])
        similarities = cosine_similarity(input_vector, self.X)
        best_match_idx = similarities.argmax()

        if similarities[0, best_match_idx] > 0.3:
            return self.dataset.iloc[best_match_idx]['Answer']
        return "(Small talk) I'm not sure how to respond to that. Please share with me something else. 😊"



    # responses = {
    #     'hi': "Hello! What's your name?",
    #     'hello': "Hey there! May I know your name?",
    #     'how are you': "I'm an AI, but I'm here to help you.",
    #     'what can you do': "I can assist with bookings, answer questions, and more!",
    #     'what is my name': "I'm sorry, I don't know your name yet. What is your name?",
    # }
    #
    # def handle(self, user_input, user_name):  # user_name=None
    #     user_input = user_input.lower()
    #     for key, response in self.responses.items():
    #         if key in user_input.lower():
    #             return response.format(user_name) if '{}' in response and user_name else response
    #     return "(Small talk) I'm not sure how to respond to that."
