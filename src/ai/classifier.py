# Optionnel : utilise scikit-learn si disponible
try:
    from sklearn.tree import DecisionTreeClassifier
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class ProfileClassifier:
    def __init__(self):
        self.model = None
        if SKLEARN_AVAILABLE:
            self.model = DecisionTreeClassifier()

    def train(self, X, y):
        if self.model:
            self.model.fit(X, y)

    def predict(self, features):
        if self.model:
            return self.model.predict([features])[0]
        # Fallback simple
        return "standard"