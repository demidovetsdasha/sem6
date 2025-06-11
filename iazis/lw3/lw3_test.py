import time
import string
import re
import matplotlib.pyplot as plt
import nltk
from nltk import pos_tag, word_tokenize, RegexpParser

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_rus')

parser = RegexpParser(
    """
    NP: {<S-PRO>?<A-PRO.*>*<A=.*>*<S>}
    P: {<PR>}
    V: {<PART>?<V.*>}
    PP: {<P> <NP>}
    VP: {<V> <NP|PP>*}
    SC: {<NP> <VP>}
    """
)

def split_into_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

def load_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def benchmark_analysis(sentences_batch):
    durations = []

    for n in range(100, 1001, 100):
        current_sentences = sentences_batch[:n]
        start_time = time.time()

        for sentence in current_sentences:
            tokens = [word for word in word_tokenize(sentence) if word not in string.punctuation]
            tagged = pos_tag(tokens, lang="rus")
            parser.parse(tagged)

        end_time = time.time()
        durations.append(end_time - start_time)

        print(f"Предложений: {n}, Время: {durations[-1]:.4f} сек")

    return list(range(100, 1001, 100)), durations

if __name__ == "__main__":
    text = load_text("test/test.txt")
    all_sentences = split_into_sentences(text)

    if len(all_sentences) < 1000:
        print(len(all_sentences))
        print("Ошибка: в файле должно быть не менее 1000 предложений.")
    else:
        x, y = benchmark_analysis(all_sentences)

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, marker='o')
        plt.title("Зависимость времени анализа от количества предложений")
        plt.xlabel("Количество предложений")
        plt.ylabel("Время (секунды)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
