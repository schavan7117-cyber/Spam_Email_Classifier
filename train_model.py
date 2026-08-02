import os
import re
import string
import joblib
import warnings

import pandas as pd
import numpy as np

import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.naive_bayes import MultinomialNB

from sklearn.svm import LinearSVC

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

warnings.filterwarnings("ignore")

# -------------------------------------------------------
# Download NLTK Data
# -------------------------------------------------------

nltk.download("stopwords")
nltk.download("wordnet")

stop_words = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()

# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

print("\nLoading dataset...\n")

data = pd.read_csv("dataset/spam.csv", encoding="latin-1")

# Keep only required columns
data = data[["v1", "v2"]]

data.columns = ["label", "message"]

print(data.head())

# -------------------------------------------------------
# Convert Labels
# -------------------------------------------------------

data["label"] = data["label"].map({
    "ham":0,
    "spam":1
})

# -------------------------------------------------------
# Text Cleaning
# -------------------------------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\\S+", "", text)

    text = re.sub(r"www\\S+", "", text)

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

print("\nCleaning text...\n")

data["message"] = data["message"].apply(clean_text)

# -------------------------------------------------------
# Dataset Statistics
# -------------------------------------------------------

print("\nDataset Statistics")

print("----------------------")

print("Total Emails :", len(data))

print("Spam :", len(data[data.label==1]))

print("Ham :", len(data[data.label==0]))

# -------------------------------------------------------
# Train Test Split
# -------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    data["message"],

    data["label"],

    test_size=0.20,

    random_state=42

)

# -------------------------------------------------------
# TF-IDF
# -------------------------------------------------------

vectorizer = TfidfVectorizer(

    max_features=5000,

    ngram_range=(1,2)

)

X_train = vectorizer.fit_transform(X_train)

X_test = vectorizer.transform(X_test)

# -------------------------------------------------------
# Models
# -------------------------------------------------------

models = {

    "Naive Bayes":

        MultinomialNB(),

    "SVM":

        LinearSVC(),

    "Logistic Regression":

        LogisticRegression(max_iter=1000),

    "Random Forest":

        RandomForestClassifier(

            n_estimators=200,

            random_state=42

        )

}

results = {}

best_accuracy = 0

best_model = None

best_name = ""

# -------------------------------------------------------
# Training
# -------------------------------------------------------

print("\nTraining Models...\n")

for name, model in models.items():

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    accuracy = accuracy_score(y_test, prediction)

    results[name] = accuracy

    print("="*50)

    print(name)

    print("="*50)

    print("Accuracy :", round(accuracy*100,2),"%")

    print()

    print(classification_report(y_test, prediction))

    print("Confusion Matrix")

    print(confusion_matrix(y_test, prediction))

    print()

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        best_model = model

        best_name = name

# -------------------------------------------------------
# Save Model
# -------------------------------------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(best_model, "models/spam_model.pkl")

joblib.dump(vectorizer, "models/vectorizer.pkl")

print("="*60)

print("Best Model :", best_name)

print("Accuracy :", round(best_accuracy*100,2),"%")

print("Model Saved Successfully!")

print("="*60)

# -------------------------------------------------------
# Model Comparison
# -------------------------------------------------------

print("\nModel Comparison")

print("-------------------------------")

for model, acc in results.items():

    print(f"{model:25} {acc*100:.2f}%")