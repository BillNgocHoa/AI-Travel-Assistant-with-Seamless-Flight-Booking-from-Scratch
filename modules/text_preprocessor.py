import re
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, ne_chunk
from nltk.tree import Tree

class TextPreprocessor:
    def __init__(self):
        # nltk.download('stopwords')
        # nltk.download('punkt')
        # nltk.download('wordnet')
        # nltk.download('averaged_perceptron_tagger')
        # nltk.download('maxent_ne_chunker')
        # nltk.download('words')
        # nltk.download('maxent_ne_chunker_tab')
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    # Tokenize the text, convert to lowercase, lemmatize, remove stopwords and non-alphanumeric characters
    def preprocess_text(self, text):
        if pd.isna(text):  # Check if the text is NaN. NaN means the text is missing
            return ""
        tokens = word_tokenize(text.lower())
        return ' '.join([
            self.lemmatizer.lemmatize(word)
            for word in tokens if word.isalnum() and word not in self.stop_words
        ])
        #return [self.lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in self.stop_words]

    # Tokenize the text, convert to lowercase, lemmatize, and remove non-alphanumeric characters
    def preprocess_text_not_remove_stopwords(self, text):
        tokens = word_tokenize(text.lower())
        return ' '.join([
            self.lemmatizer.lemmatize(word)
            for word in tokens if word.isalnum()
        ])

    def detect_location(self, text):
        """
        Detects locations in user input using Named Entity Recognition (NER).
        """
        # Tokenize and tag parts of speech
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)

        # Perform Named Entity Recognition (NER)
        chunks = ne_chunk(pos_tags, binary=False)

        # Extract location entities (GPE: Geo-Political Entity)
        locations = []
        for chunk in chunks:
            if isinstance(chunk, Tree) and chunk.label() == 'GPE':  # GPE: Locations like cities, countries, etc.
                location = " ".join(c[0] for c in chunk)
                locations.append(location)

        return locations if locations else None

    def detect_name(self, text):
        """
        Detects names in user input using Named Entity Recognition (NER).
        """
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        chunks = ne_chunk(pos_tags, binary=False)

        # Extract person entities (PERSON label)
        names = []
        for chunk in chunks:
            if isinstance(chunk, Tree) and chunk.label() == 'PERSON':
                name = " ".join(c[0] for c in chunk)
                names.append(name)

        return names if names else None

    def detect_age(self, text):
        """
        Detects age from user input, either as a number or written in words.
        """
        # Map written numbers to digits
        number_words = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
            'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
            'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40,
            'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80,
            'ninety': 90
        }

        # Match ages written as numbers
        number_match = re.search(r'\b(\d{1,2})\b', text)
        if number_match:
            age = int(number_match.group(1))
            if 0 < age < 120:  # Age validation range
                return age

        # Match ages written as words
        tokens = word_tokenize(text.lower())
        age_in_words = [number_words[token] for token in tokens if token in number_words]

        if age_in_words:
            total_age = sum(age_in_words)
            if 0 < total_age < 120:
                return total_age

        return None


if __name__ == "__main__":
    preprocessor = TextPreprocessor()

    # Test location detection
    # user_input = "I would like to have a travel to Bali please."
    # detected_locations = preprocessor.detect_location(user_input)
    # print(f"Detected locations: {detected_locations}")

    # Test name detection
    sentence_with_name = "Hello, call me bill and I would like to book a flight."
    detected_names = preprocessor.detect_name(sentence_with_name)
    print(f"Detected names: {detected_names}")

    # Test age detection
    sentence_with_age_number = "I am forty two years old."
    detected_age_number = preprocessor.detect_age(sentence_with_age_number)
    print(f"Detected age (number): {detected_age_number}")

    sentence_with_age_words = "I am sixty five years old."
    detected_age_words = preprocessor.detect_age(sentence_with_age_words)
    print(f"Detected age (words): {detected_age_words}")


    # Integration to detect age and name in chatbot
    '''
    print("Chatbot: Could you please tell me your name?")
    name_input = input("User: ")
    detected_names = self.text_preprocessor.detect_name(name_input)
    user_name = detected_names[0] if detected_names else "User"
    print(f"Chatbot: Nice to meet you, {user_name}!")

    print("Chatbot: How old are you?")
    age_input = input("User: ")
    detected_age = self.text_preprocessor.detect_age(age_input)
    if detected_age:
        print(f"Chatbot: Thank you for sharing your age, {detected_age} years old!")
    else:
        print("Chatbot: I couldn't detect your age. Could you clarify?")
    '''