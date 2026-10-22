"""A bounded text assistant: intent classification and predefined answers."""
from pathlib import Path
import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

from chatbot_data import TOPICS

FALLBACK = (
    "I could not confidently match that question to a supported topic. "
    "Try one question about AgriPredict, model results, maize planting, soil, irrigation, "
    "fertiliser, rotation or crop problems. I do not cover all agriculture topics."
)
# Similarity cutoffs are heuristics, not calibrated confidence probabilities.
MIN_SIMILARITY = 0.30
MIN_TOPIC_GAP = 0.08
examples = [(text, intent) for intent, (questions, _) in TOPICS.items() for text in questions]
vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
example_vectors = vectorizer.fit_transform([text for text, _ in examples])
classifier = LogisticRegression(C=4, max_iter=1000, random_state=42)
classifier.fit(example_vectors, [intent for _, intent in examples])


def classify(question):
    if not isinstance(question, str) or not question.strip() or len(question) > 1000:
        return None
    query = vectorizer.transform([question])
    similarities = cosine_similarity(query, example_vectors)[0]
    scores = {intent: max(similarities[i] for i, (_, label) in enumerate(examples)
                          if label == intent) for intent in TOPICS}
    ranked = sorted(scores, key=scores.get, reverse=True)
    predicted = classifier.predict(query)[0]
    # Require both methods to agree; decline ambiguous or unfamiliar wording.
    if (scores[ranked[0]] < MIN_SIMILARITY
            or scores[ranked[0]] - scores[ranked[1]] < MIN_TOPIC_GAP
            or predicted != ranked[0]):
        return None
    return predicted


def performance_answer(results_path=None):
    path = (Path(results_path) if results_path is not None else
            Path(__file__).resolve().parent.parent / "Results" / "model_metrics.csv")
    try:
        metrics = pd.read_csv(path)
        needed = {"split", "model", "MAE", "RMSE"}
        if not needed.issubset(metrics.columns):
            return TOPICS["performance"][1]
        baseline = metrics[(metrics["split"] == "Test") &
                           (metrics["model"] == "Historical baseline")]
        if len(baseline) != 1:
            return TOPICS["performance"][1]
        mae, rmse = float(baseline.iloc[0]["MAE"]), float(baseline.iloc[0]["RMSE"])
        if not (0 <= mae < float("inf") and 0 <= rmse < float("inf")):
            return TOPICS["performance"][1]
    except (OSError, ValueError, TypeError, pd.errors.ParserError):
        return TOPICS["performance"][1]
    return (f"The historical baseline's test MAE is {mae:.3f} and RMSE is {rmse:.3f} "
            "tonnes per planted hectare, read from the saved evaluation results. "
            "Lower values mean smaller errors. These are historical test scores, not a guarantee for a new season.")


def respond(question):
    if isinstance(question, str) and re.fullmatch(r"\s*(hi|hello|hey)[!.\s]*", question.lower()):
        return "Hello! Ask me about AgriPredict or a supported maize farming topic."
    intent = classify(question)
    if intent is None:
        return FALLBACK
    if intent == "performance":
        return performance_answer()
    return TOPICS[intent][1]


def run_chatbot():
    print("AgriPredict text assistant. Type 'quit' to exit.")
    while True:
        try:
            question = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if question.strip().lower() in {"quit", "exit", "bye"}:
            break
        print("AgriPredict:", respond(question))


if __name__ == "__main__":
    run_chatbot()
