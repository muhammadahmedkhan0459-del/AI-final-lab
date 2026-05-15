import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

CSV_PATH   = "data/final_eval.csv"
MODEL_PATH = "models/semantic_model.joblib"

def load_training_data():
    df = pd.read_csv(CSV_PATH)
    df["label"] = df["expected_policy"].apply(lambda x: 1 if x == "BLOCK" else 0)
    texts  = df["prompt"].tolist()
    labels = df["label"].tolist()
    return texts, labels

def train_and_save():
    os.makedirs("models", exist_ok=True)

    texts, labels = load_training_data()

    # Split: 80% train, 20% test
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
        ("clf",   LogisticRegression(max_iter=1000))
    ])

    pipeline.fit(train_texts, train_labels)

    # Show quick accuracy on the 20% test portion
    accuracy = pipeline.score(test_texts, test_labels)
    print(f"[Semantic Model] Trained on {len(train_texts)} examples")
    print(f"[Semantic Model] Test accuracy: {accuracy:.2%}")

    joblib.dump(pipeline, MODEL_PATH)
    print(f"[Semantic Model] Saved to {MODEL_PATH}")

    return pipeline

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return train_and_save()

_model = None

def get_semantic_score(text: str) -> float:
    """Returns a 0.0 to 1.0 risk score. Higher means more likely an attack."""
    global _model
    if _model is None:
        _model = load_model()
    prob = _model.predict_proba([text])[0][1]
    return round(float(prob), 4)
