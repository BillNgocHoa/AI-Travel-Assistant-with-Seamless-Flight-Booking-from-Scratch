from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class QuestionAnswering:
    def __init__(self, dataset):
        self.dataset = dataset
        #self.preprocessor = preprocessor
        self.vectorizer = TfidfVectorizer()
        self.X = self.vectorizer.fit_transform(self.dataset['Processed_Question'])  # 'Processed_Question' is the column name in the dataset that contains the preprocessed questions

    def find_answer(self, user_input, preprocessor):
        processed_input = preprocessor.preprocess_text(user_input)
        input_vector = self.vectorizer.transform([processed_input])
        similarities = cosine_similarity(input_vector, self.X)
        best_match_idx = similarities.argmax()

        if similarities[0, best_match_idx] > 0.3:
            return self.dataset.iloc[best_match_idx]['Answer']
        return "(QA) Sorry, I couldn't find an answer to your question. Could you please rephrase it?"
