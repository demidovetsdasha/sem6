import spacy
import time
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog


nlp = spacy.load("ru_core_news_sm")

def load_text_from_file():
    root = Tk()
    root.withdraw()  
    file_path = filedialog.askopenfilename(
        title="Выберите текстовый файл",
        filetypes=[("Text files", "*.txt")]
    )
    if not file_path:
        print("Файл не выбран.")
        exit()

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


text = load_text_from_file()

# Разбиваем исходный текст на предложения
doc = nlp(text)
sentences = list(doc.sents)

# Определяем пороги количества предложений для теста
step = max(1, len(sentences) // 7)
sentence_counts = list(range(step, len(sentences) + 1, step))
processing_times = []

print("\nОценка производительности...")
for count in sentence_counts:
    sub_text = " ".join(str(s) for s in sentences[:count])
    start = time.time()
    _ = nlp(sub_text)
    end = time.time()
    duration = end - start
    processing_times.append(duration)
    print(f"{count} предложений: {duration:.3f} сек")

plt.figure(figsize=(10, 6))
plt.plot(sentence_counts, processing_times, marker="o", linestyle="-", color="darkblue")
plt.title("Зависимость времени синтаксического анализа от количества предложений")
plt.xlabel("Количество предложений")
plt.ylabel("Время анализа (сек.)")
plt.grid(True)
plt.tight_layout()
plt.show()
