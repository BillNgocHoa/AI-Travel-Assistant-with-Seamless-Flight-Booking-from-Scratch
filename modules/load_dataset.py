import pandas as pd
from .text_preprocessor import TextPreprocessor

class LoadDataset:
    def __init__(self):
        self.preprocessor = TextPreprocessor()

    def load_and_preprocess(self, file_path, column_name):
        # Load dataset
        dataset = pd.read_csv(file_path)
        # Preprocess the specified column
        dataset[f'Processed_{column_name}'] = dataset[column_name].apply(self.preprocessor.preprocess_text)
        # Save the preprocessed qa_dataset to a new CSV file
        dataset.to_csv(f'Preprocessed_{column_name}_Dataset.csv', index=False)
        return dataset

    def load_and_preprocess_not_remove_stopwords(self, file_path, column_name):
        # Load dataset
        dataset = pd.read_csv(file_path)
        # Preprocess the specified column
        dataset[f'Processed_{column_name}'] = dataset[column_name].apply(self.preprocessor.preprocess_text_not_remove_stopwords)
        # Save the preprocessed qa_dataset to a new CSV file
        dataset.to_csv(f'Preprocessed_{column_name}_Dataset.csv', index=False)
        return dataset

    @staticmethod  # This method does not require an instance of the class to be created
    def load_csv(file_path):
        return pd.read_csv(file_path)
