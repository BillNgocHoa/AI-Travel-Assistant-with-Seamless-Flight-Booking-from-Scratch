from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class IntentClassifier:
    def __init__(self, dataset):
        self.dataset = dataset
        #self.preprocessor = preprocessor
        self.vectorizer = TfidfVectorizer()
        self.X = self.vectorizer.fit_transform(self.dataset['Processed_User_Input'])

    def classify(self, user_input, preprocessor):
        #processed_input = preprocessor.preprocess_text(user_input)  # (in older code) is: 'intent_dataset['Processed_Input'] = intent_dataset['User_Input'].apply(preprocess_text)'
        processed_input = preprocessor.preprocess_text_not_remove_stopwords(user_input)
        input_vector = self.vectorizer.transform([processed_input])
        similarities = cosine_similarity(input_vector, self.X)
        best_match_idx = similarities.argmax()

        if similarities[0, best_match_idx] > 0.3:
            return self.dataset.iloc[best_match_idx]['Intent']
        return '(Intent Handler) unknown intent'

# Intent Matching Function
# intents = {
#     'booking': ['book', 'reserve', 'schedule'],
#     'identity': ['my name is', 'call me'], # 'name'
#     'small_talk': ['hello', 'hi', 'how are you', 'what can you do', 'what is my name'],
#     'question': ['how', 'what', 'why', 'where', 'when']
# }
#
# def get_intent(user_input):
#     user_input = user_input.lower()
#     for intent, keywords in intents.items():
#         if any(keyword in user_input.lower() for keyword in keywords):
#             return intent
#     return 'unknown'