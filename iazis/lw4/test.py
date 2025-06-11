from SentencesWindow import SentencesWindow
import time
import tkinter as tk
from unittest.mock import MagicMock
import matplotlib.pyplot as plt

def test_semantic_analysis_performance():
    text = (
        "Мама мыла раму. Папа читал газету. Дети играли во дворе. "
        "Кошка спала на подоконнике. Солнце светило ярко. "
        "Птицы пели в саду. Машина проехала мимо. Дождь пошел внезапно. "
        "Зонта не было. Люди бежали по улице. Все промокли до нитки."
    )

    root = tk.Tk()
    root.withdraw()

    app = SentencesWindow(root, text)

    app.semantic_analysis = MagicMock(side_effect=app.semantic_analysis)

    counts = []
    timings = []

    # Прогоним анализ для 1..10 предложений
    for i in range(1, 11):
        sentences_subset = app.sentences[:i]

        # Очистим и заново заполним дерево (на случай перезапуска)
        app.tree.delete(*app.tree.get_children())
        for sent in sentences_subset:
            app.tree.insert("", "end", values=(sent,))

        # Засекаем время анализа
        start_time = time.time()
        for item_id in app.tree.get_children():
            app.tree.selection_set(item_id)
            app.semantic_analysis()
        elapsed_time = time.time() - start_time

        print(f"⏱ Время анализа для {i} предложений: {elapsed_time:.4f} секунд")

        counts.append(i)
        timings.append(elapsed_time)

    # Построим график после всех измерений
    plt.figure(figsize=(10, 6))
    plt.plot(counts, timings, marker='o', linestyle='-', color='royalblue')
    plt.title("Производительность семантического анализа")
    plt.xlabel("Количество предложений")
    plt.ylabel("Время выполнения (секунды)")
    plt.grid(True)
    plt.xticks(counts)
    plt.tight_layout()
    plt.show()

test_semantic_analysis_performance()
