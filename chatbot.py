import nltk
from nltk import pos_tag, ne_chunk
from nltk.tree import Tree
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('words')
nltk.download('universal_tagset')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('maxent_ne_chunker')
nltk.download('maxent_ne_chunker_tab')

from modules.load_dataset import LoadDataset
from modules.text_preprocessor import TextPreprocessor
from modules.intent_classifier import IntentClassifier
from modules.question_answering import QuestionAnswering
from modules.small_talk_handler import SmallTalkHandler
from modules.identity_manager import IdentityManager
from modules.booking_process import BookingProcess, BookingDetailsManager
from modules.person import Person


def chatbot():

    user_general = Person()

    # Initialize Preprocessor
    preprocessor = TextPreprocessor()

    # Load and preprocess datasets
    loader = LoadDataset()
    qa_dataset = loader.load_and_preprocess('datasets/COMP3074-CW1-Dataset.csv', 'Question')
    intent_dataset = loader.load_and_preprocess_not_remove_stopwords('datasets/All-Info-Dataset.csv', 'User_Input')
    small_talk_dataset = loader.load_and_preprocess_not_remove_stopwords('datasets/Small-Talk-Dataset.csv', 'User_Input')
    identity_dataset = loader.load_and_preprocess_not_remove_stopwords('datasets/Identity-Dataset.csv', 'User_Input')
    flight_database = 'datasets/Flight-DB.csv'

    # Initialize components
    intent_classifier = IntentClassifier(intent_dataset)
    question_answerer = QuestionAnswering(qa_dataset)
    small_talk_handler = SmallTalkHandler(small_talk_dataset)
    identity_manager = IdentityManager(identity_dataset, user_general)
    booking_process = BookingProcess(flight_database, user_general)

    print("Chatbot: Welcome to the SkyTravel! I'm am your flight booking assistant. I can:    \n"
          "         - Book a flight ticket for you 🛫   \n"
          "         - Have a small chat with you     \n"
          "         - Answer your general questions, like 'When did World war 2 end?' \n") # How can I assist you today?

    print("Quick note: you can type 'exit' or 'quit' to STOP the conversation at any time.\n")

    print("Chatbot: Alright, that's it for a long introduction, haha 😊\n"
          "         How should I call you?")
    while user_general.get_name() is None:
        name_input = input("User: ")
        response = identity_manager.handle_identity(name_input, preprocessor)
        print(f"Chatbot: {response}")

    print("Chatbot: How can I assist you today? 💖")


    while True:
        user_input_original = input("User: ")
        user_input = user_input_original.lower()
        if user_input in ['exit', 'quit']:
            print("Chatbot: It was nice to chat with you. \n"
                  "         Enjoy your day 😊.Goodbye!")
            break

        intent = intent_classifier.classify(user_input, preprocessor)

        if intent == 'small_talk':
            response = small_talk_handler.find_answer(user_input, preprocessor)  # 2nd item: identity_manager.get_user_name()
        elif intent == 'booking':
            if user_general.get_name():
                booking_process.start_booking()
                response = "Do you need any further support? If you're not sure, just ask:\n\t\t 'What can you do?'."
            else:
                response = "Sure. And before we start, how may I call you?"
        elif intent == 'identity':
            response = identity_manager.handle_identity(user_input_original, preprocessor)
        elif intent == 'question':
            response = question_answerer.find_answer(user_input, preprocessor)
        else:
            response = "Sorry, I didn't recognise that. Could you please rephrase it?"

        print(f"Chatbot: {response}")


if __name__ == "__main__":
    chatbot()
