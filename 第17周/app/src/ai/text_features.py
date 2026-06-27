from sklearn.feature_extraction.text import TfidfVectorizer

class TextFeatureExtractor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            max_features=500
        )

    def fit(self, texts):
        self.vectorizer.fit(texts)

    def transform(self, texts):
        return self.vectorizer.transform(texts)

    def fit_transform(self, texts):
        return self.vectorizer.fit_transform(texts)
