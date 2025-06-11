import json
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer  # Замена pymorphy3
import string
import nltk

nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()


with open("animals_keywords.json", encoding="utf-8") as f:
    raw_keywords = json.load(f)["keywords"]
    lemmatized_keywords = set(
        lemmatizer.lemmatize(word.lower()) for word in raw_keywords
    )

def is_animals_question(text: str) -> bool:
    tokens = word_tokenize(text.lower(), language="english")  
    lemmas = [
        lemmatizer.lemmatize(token)  
        for token in tokens
        if token not in string.punctuation
    ]
    return any(lemma in lemmatized_keywords for lemma in lemmas)