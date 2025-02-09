import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK data
nltk.download("punkt")

# Load chatbot training data
csv_file = "data/chatbot_training_data.csv"  # Ensure this file is in the 'data/' folder
df = pd.read_csv(csv_file)

def chatbot_response(user_input):
    """Process user input and return the best chatbot response based on similarity."""
    df_combined = df.copy()
    df_combined.loc[len(df_combined)] = ["user_query", user_input, ""]  # Add user input

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df_combined["question"])

    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_match_idx = similarities.argsort()[0][-1]

    return df.loc[best_match_idx, "answer"]

# Chatbot interaction
print("Chatbot: Hello! Ask me anything about SQL queries. Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Chatbot: Goodbye!")
        break
    response = chatbot_response(user_input)
    print(f"Chatbot: {response}")
