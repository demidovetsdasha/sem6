import time
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import spacy
from wiki_ru_wordnet import WikiWordnet
from pymorphy3 import MorphAnalyzer

# Инициализация библиотек
nlp = spacy.load("ru_core_news_sm")
wikiwordnet = WikiWordnet()
morph = MorphAnalyzer()

# Получение семантической информации
def get_semantic_info(word):
    base_form = morph.parse(word)[0].normal_form
    synsets = list(wikiwordnet.get_synsets(base_form))

    if synsets:
        first_synset = synsets[0]
        words_set = first_synset.get_words()
        words = list(words_set)
        definition = words[0].definition() if words else "—"
        synonyms = [w.lemma() for s in synsets for w in s.get_words()]
        hypernyms = [w.lemma() for h in wikiwordnet.get_hypernyms(first_synset) for w in h.get_words()]
    else:
        definition = "—"
        synonyms = []
        hypernyms = []

    return {
        "word": word,
        "definition": definition,
        "synonyms": synonyms,
        "hypernyms": hypernyms
    }

# Анализ предложений и замер времени
def analyze_sentences(sentences, step):
    times = []
    sizes = []

    for i in range(step, len(sentences) + 1, step):
        subset = sentences[:i]
        start = time.time()

        for sent in subset:
            doc = nlp(sent)
            for token in doc:
                if token.is_alpha:
                    get_semantic_info(token.text)

        end = time.time()
        sizes.append(i)
        times.append(end - start)
        print(f"Обработано {i} предложений за {end - start:.2f} сек.")

    return sizes, times

# Запуск бенчмарка
def run_benchmark():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Выберите текстовый файл", filetypes=[("Text files", "*.txt")])
    if not file_path:
        print("Файл не выбран.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    step = max(1, len(sentences) // 10)

    sizes, times = analyze_sentences(sentences, step)

    # Построение графика
    plt.plot(sizes, times, marker='o')
    plt.xlabel("Количество предложений")
    plt.ylabel("Время анализа (сек.)")
    plt.title("Зависимость времени семантического анализа от размера текста")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Запуск
if __name__ == "__main__":
    run_benchmark()
