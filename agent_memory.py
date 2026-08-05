from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

TABLE_SCHEMAS = {
    "users": "Contains employee profiles, user ids, names, roles, and join dates.",
    "sales": "Contains financial transactions, transaction ids, user ids, dollar amounts, and product names purchased."
}

def get_relevant_schema(user_query: str) -> str:
    # Clean text-matching vector engine
    vectorizer = TfidfVectorizer()

    tables = list(TABLE_SCHEMAS.keys())
    descriptions = list(TABLE_SCHEMAS.values())

    # Fit and calculate similarity scores natively
    tfidf_matrix = vectorizer.fit_transform(descriptions + [user_query])

    # Compare descriptions against user query
    scores = cosine_similarity(tfidf_matrix[:-1], tfidf_matrix[-1])

    best_index = scores.flatten().argmax()
    return tables[best_index]