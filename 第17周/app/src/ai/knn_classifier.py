from sklearn.neighbors import KNeighborsClassifier

class KNNTextClassifier:
    def __init__(self, k=5):
        self.k = k
        self.model = KNeighborsClassifier(n_neighbors=k)

    def train(self, X, y):
        """Train the KNN classifier with training data"""
        self.model.fit(X, y)

    def predict(self, X):
        """Predict single or batch samples"""
        return self.model.predict(X)[0]
    
    def predict_batch(self, X):
        """Predict batch of samples and return all predictions"""
        return self.model.predict(X)
