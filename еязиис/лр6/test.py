import time
import matplotlib.pyplot as plt
from dialog_system import get_answer_tfidf, save_qa_to_file

# --- Заглушка для внешней языковой модели (имитируем задержку) ---
def mock_llm_response(question):
    time.sleep(0.8)  # Имитируем задержку ответа LLM (например, 800 мс)
    return f"LLM-generated answer for: {question}"

# --- Вопросы, часть есть в базе, часть новых ---
predefined_questions = [
    "How does bioluminescence help deep-sea creatures survive in complete darkness?",
    "Do insects have bones?",
    "What is mimicry in animals?"
]

new_questions = [
    "Can penguins fly?",
    "How do elephants use their trunks?",
    "What is the fastest land animal?"
]


# --- Основная функция сравнения ---
def compare_performance():
    tfidf_times = []
    llm_times = []

    # Запросы с уже известными вопросами
    for q in predefined_questions:
        start = time.time()
        _ = get_answer_tfidf(q)
        elapsed = time.time() - start
        tfidf_times.append(elapsed)
        print(f"[TF-IDF] {q} — {elapsed:.4f} sec")

    # Запросы, которых нет в базе, используем заглушку LLM
    for q in new_questions:
        start = time.time()
        answer = get_answer_tfidf(q)
        if answer is None:
            answer = mock_llm_response(q)
            save_qa_to_file(q, answer)
        elapsed = time.time() - start
        llm_times.append(elapsed)
        print(f"[LLM] {q} — {elapsed:.4f} sec")

    return tfidf_times, llm_times

# --- Построение графика ---
if __name__ == "__main__":
    tfidf, llm = compare_performance()

    labels = ["TF-IDF"] * len(tfidf) + ["LLM"] * len(llm)
    times = tfidf + llm

    plt.figure(figsize=(10, 6))
    plt.bar(labels, times, color=["green"] * len(tfidf) + ["blue"] * len(llm))
    plt.title("Сравнение времени ответа: TF-IDF vs LLM")
    plt.ylabel("Время ответа (сек)")
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig("response_time_comparison.png")
    plt.show()
