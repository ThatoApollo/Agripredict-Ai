from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from chatbot_data import ASSISTANT_HELP_QUESTIONS, FALLBACK, INTENTS

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
    examples = vectorizer.fit_transform(questions)
    classifier = LogisticRegression(C=20, max_iter=1000, random_state=42)
    classifier.fit(examples, topics)
    return vectorizer, classifier, examples, topics


def respond(question, model):
    if not isinstance(question, str) or not question.strip():
        return 'Please type a question.', None, 0.0
    if len(question) > 1000:
        return 'Please ask one short question, under 1,000 characters.', None, 0.0
    clean_question = question.strip().lower()
    if clean_question in ['hi', 'hello', 'hey']:
        return 'Hello! Ask what I can do, or ask about AgriPredict, its results or a supported maize topic.', 'greeting', 0.0
    if clean_question.rstrip('?! .') in ASSISTANT_HELP_QUESTIONS:
        return INTENTS['assistant_help']['answer'], 'assistant_help', 0.0
    if ' and ' in clean_question:
        first, second = clean_question.split(' and ', 1)
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

    # Find the closest example for each topic.
    similarities = cosine_similarity(query, examples)[0]
    scores = {}
    for label, similarity in zip(topics, similarities):
        scores[label] = max(scores.get(label, 0.0), float(similarity))
    ranked = sorted(scores, key=scores.get, reverse=True)
    closest, second = ranked[:2]
    gap = scores[closest] - scores[second]
    if confidence < MIN_PROBABILITY or scores[closest] < MIN_SIMILARITY:
        return FALLBACK, None, confidence
    if topic != closest or gap < MIN_TOPIC_GAP:
        return FALLBACK, None, confidence
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
