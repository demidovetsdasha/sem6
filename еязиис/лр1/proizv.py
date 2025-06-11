import os
import spacy
import time
from docx import Document
import matplotlib.pyplot as plt

def process_docx(file_path):
    nlp = spacy.load("en_core_web_sm")
    docx_file = Document(file_path)

    text = "\n".join([para.text for para in docx_file.paragraphs])

    start_nlp = time.time()
    _ = nlp(text)
    end_nlp = time.time()

    return end_nlp - start_nlp, len(text.split())

if __name__ == "__main__":
    # Получаем папку, где лежит сам скрипт
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Список файлов для теста
    file_names = [
        "short_text.docx",
        "large_text.docx"
    ]

    sizes = []
    times = []

    for name in file_names:
        path = os.path.join(script_dir, name)
        if os.path.exists(path):
            nlp_time, word_count = process_docx(path)
            sizes.append(word_count)
            times.append(nlp_time)
            print(f"{name}: {word_count} слов — {nlp_time:.4f} сек.")
        else:
            print(f"Файл не найден: {path}")

    if sizes and times:
        plt.figure(figsize=(8, 5))
        plt.plot(sizes, times, marker='o', linestyle='-')
        plt.title('Время обработки в завивисимости от размера текста')
        plt.xlabel('Количество слов')
        plt.ylabel('Время обработки (сек.)')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
