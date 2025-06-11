import json
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer  # Замена pymorphy3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

english_stopwords = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()  # Замена MorphAnalyzer


def preprocess(text):
    text = text.lower()
    tokens = word_tokenize(text, language="english")
    lemmas = [
        lemmatizer.lemmatize(word)  
        for word in tokens
        if word.isalnum() and word not in english_stopwords
    ]
    return " ".join(lemmas)


def get_answer_tfidf(user_question, threshold=0.6):
    with open("qa.json", encoding="utf-8") as f:
        qa_data = json.load(f)

    questions = [qa["question"] for qa in qa_data]
    answers = [qa["answer"] for qa in qa_data]

    # Предобработка вопросов
    processed_questions = [preprocess(q) for q in questions]
    processed_input = preprocess(user_question)
    print(processed_input)
    print(processed_questions)

    # TF-IDF векторизация
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(processed_questions + [processed_input])

    # Последний вектор — это пользовательский вопрос
    similarities = cosine_similarity(vectors[-1], vectors[:-1])[0]

    best_index = similarities.argmax()
    best_score = similarities[best_index]
    print(best_score)

    if best_score >= threshold:
        return answers[best_index]
    else:
        return None


def save_qa_to_file(question: str, answer: str, filename: str = "qa.json"):
    """Сохраняет вопрос и ответ в JSON-файл."""
    qa_entry = {
        "question": question,
        "answer": answer
    }

    # Если файл существует, загрузим старые данные
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(qa_entry)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

