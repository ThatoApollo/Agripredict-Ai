"""Topic classification and predefined answers. Run: python Code/chatbot.py"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

import settings
from chatbot_data import ASSISTANT_HELP_QUESTIONS, FALLBACK, INTENTS

# Heuristics, not calibrated probabilities that an answer is correct.
MIN_PROBABILITY = 0.30
MIN_SIMILARITY = 0.30
MIN_TOPIC_GAP = 0.08


def build_classifier():
    questions = []
    topics = []
    for topic, intent in INTENTS.items():
        for question in intent['examples']:
            questions.append(question)
            topics.append(topic)
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    example_vectors = vectorizer.fit_transform(questions)
    # This classifier matches questions to topics; it does not predict crop yield.
    classifier = LogisticRegression(C=20, max_iter=1000, random_state=42)
    classifier.fit(example_vectors, topics)
    return vectorizer, classifier, example_vectors, topics


def performance_answer(results_dir=None):
    if results_dir is None:
        results_dir = settings.PROJECT_DIR / 'Results'
    path = Path(results_dir) / 'test_metrics.csv'
    unavailable = 'Saved model results are unavailable or invalid. Run Code/yield_model.py to recreate them.'
    try:
        metrics = pd.read_csv(path)
        for column in ['model', 'MAE', 'RMSE']:
            if column not in metrics.columns:
                return unavailable
        if metrics.empty or metrics['model'].isna().any() or metrics['model'].duplicated().any():
            return unavailable
        for column in ['MAE', 'RMSE']:
            metrics[column] = pd.to_numeric(metrics[column], errors='raise')
            if not np.isfinite(metrics[column]).all() or (metrics[column] < 0).any():
                return unavailable
        model_names = metrics['model'].tolist()
        if 'Historical baseline' not in model_names or 'Linear regression' not in model_names:
            return unavailable
    except (OSError, ValueError, TypeError, pd.errors.ParserError):
        return unavailable

    lines = ['Recorded 2020 errors, in tonnes per hectare:']
    for _, row in metrics.iterrows():
        lines.append(f"{row['model']}: MAE {row['MAE']:.3f}, RMSE {row['RMSE']:.3f}.")
    baseline_results = metrics[metrics['model'] == 'Historical baseline'].iloc[0]
    linear_results = metrics[metrics['model'] == 'Linear regression'].iloc[0]
    if linear_results['MAE'] < baseline_results['MAE']:
        lines.append('Linear regression had lower recorded test MAE than the baseline.')
    elif linear_results['MAE'] > baseline_results['MAE']:
        lines.append('The historical baseline had lower recorded test MAE than linear regression.')
    else:
        lines.append('Linear regression and the baseline had equal recorded test MAE.')
    lines.append('Linear regression was adopted for simplicity after test results were known. These are historical scores, not a new independent test or a guarantee for another field.')
    return '\n'.join(lines)


def respond(question, model):
    if not isinstance(question, str) or not question.strip():
        return 'Please type a question.', None, 0.0
    if len(question) > 1000:
        return 'Please ask one short question, under 1,000 characters.', None, 0.0
    if question.strip().lower() in ['hi', 'hello', 'hey']:
        return 'Hello! Ask what I can do, or ask about AgriPredict, its results or a supported maize topic.', 'greeting', 0.0

    # Recognise short help questions that lose key words during vectorisation.
    help_question = question.strip().lower().rstrip('?! .')
    if help_question in ASSISTANT_HELP_QUESTIONS:
        return INTENTS['assistant_help']['answer'], 'assistant_help', 0.0

    # Decline clearly separate supported topics in one message.
    if ' and ' in question.lower():
        first, second = question.lower().split(' and ', 1)
        _, first_topic, _ = respond(first, model)
        _, second_topic, _ = respond(second, model)
        if first_topic is not None and second_topic is not None and first_topic != second_topic:
            return 'Please ask one topic at a time.', None, 0.0

    vectorizer, classifier, examples, topics = model
    query = vectorizer.transform([question])
    probabilities = classifier.predict_proba(query)[0]
    best_index = probabilities.argmax()
    topic = classifier.classes_[best_index]
    confidence = float(probabilities[best_index])
    similarities = cosine_similarity(query, examples)[0]
    topic_scores = {}
    for index, label in enumerate(topics):
        if label not in topic_scores:
            topic_scores[label] = 0.0
        topic_scores[label] = max(topic_scores[label], float(similarities[index]))
    ranked_topics = sorted(topic_scores, key=topic_scores.get, reverse=True)
    topic_gap = topic_scores[ranked_topics[0]] - topic_scores[ranked_topics[1]]
    if confidence < MIN_PROBABILITY or topic_scores[ranked_topics[0]] < MIN_SIMILARITY:
        return FALLBACK, None, confidence
    if topic != ranked_topics[0] or topic_gap < MIN_TOPIC_GAP:
        return FALLBACK, None, confidence
    if topic == 'performance':
        return performance_answer(), topic, confidence
    return INTENTS[topic]['answer'], topic, confidence


def main():
    model = build_classifier()
    print('AgriPredict assistant. Type quit to exit.')
    while True:
        try:
            question = input('You: ')
        except (EOFError, KeyboardInterrupt):
            break
        if question.strip().lower() in ['quit', 'exit']:
            break
        answer, _, _ = respond(question, model)
        print('AgriPredict:', answer)


if __name__ == '__main__':
    main()
