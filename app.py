import os
print("Running from:", os.getcwd())
print("This file:", __file__)

from flask import Flask, render_template, request, redirect
import joblib
import re
import string
import nltk
import numpy as np

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from database import (
    create_database,
    insert_prediction,
    get_history,
    delete_history
)

# -----------------------------
# Download NLTK Resources
# -----------------------------
nltk.download("stopwords")
nltk.download("wordnet")

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("models/spam_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

app = Flask(__name__)

# Create database
create_database()

# -----------------------------
# Text Cleaning
# -----------------------------
def clean_text(text):
    text = text.lower()

    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\d+", "", text)

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    words = text.split()

    words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words
    ]

    return " ".join(words)


# -----------------------------
# Home
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Predict
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    email = request.form["email"]

    cleaned = clean_text(email)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]

    # -----------------------------
    # Confidence Score
    # -----------------------------
    confidence = 0

    if hasattr(model, "predict_proba"):

        confidence = (
            max(model.predict_proba(vector)[0]) * 100
        )

    elif hasattr(model, "decision_function"):

        score = model.decision_function(vector)[0]

        confidence = (
            1 / (1 + np.exp(-abs(score)))
        ) * 100

    if prediction == 1:

        result = "🚨 SPAM EMAIL"

    else:

        result = "✅ NOT SPAM"

    # Save into database
    insert_prediction(
        email,
        result,
        round(confidence, 2)
    )

    return render_template(
        "index.html",
        prediction=result,
        confidence=round(confidence, 2),
        email=email
    )


# -----------------------------
# History
# -----------------------------
@app.route("/history")
def history():

    history = get_history()

    return render_template(
        "history.html",
        history=history
    )


# -----------------------------
# Clear History
# -----------------------------
@app.route("/clear-history")
def clear_history():

    delete_history()

    return redirect("/history")


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)