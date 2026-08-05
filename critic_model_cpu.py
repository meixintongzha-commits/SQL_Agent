import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier

class NativeAgentCritic:
    def __init__(self):
        # Initialize text vectorizer and a dynamic online learning model
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.model = SGDClassifier(loss="log_loss", learning_rate="constant", eta0=0.1)
        self.is_trained = False
        
        # Pre-seed vectorizer with basic SQL tokens so it handles fresh inputs safely
        initial_corpus = ["SELECT * FROM users", "SELECT amount FROM sales JOIN users", "DROP TABLE"]
        self.vectorizer.fit(initial_corpus)

    def predict_success_rate(self, sql_text: str) -> float:
        """Calculates a mathematical probability score between 0.0 and 1.0."""
        if not self.is_trained:
            return 0.50  # Neutral starting confidence before any feedback data arrives
            
        features = self.vectorizer.transform([sql_text])
        # Return probability score for the 'Success' class (Index 1)
        probabilities = self.model.predict_proba(features)
        return float(probabilities[0][1])

    def update_model(self, sql_text: str, success: bool):
        """Live feedback step: Updates weights instantly using real runtime feedback."""
        features = self.vectorizer.transform([sql_text])
        target_label = np.array([1 if success else 0])
        
        # partial_fit lets the model update its weights incrementally without needing a huge database
        self.model.partial_fit(features, target_label, classes=np.array([0, 1]))
        self.is_trained = True

# Instantiate a single global critic tracking object
critic = NativeAgentCritic()
