from collections import Counter
import json
import spacy
import re
import time
import os
import xml.etree.ElementTree as ET
from glob import glob
from collections import Counter

class DataExtractor:
    def __init__(self):
        self.load_config()
        self.data_file = self.config["DATA_FILE"]
        self.case_map = self.config["CASE_MAP"]
        self.pos_map = self.config["POS_MAP"]
        self.number_map = self.config["NUMBER_MAP"]
        self.gender_map = self.config["GENDER_MAP"]

    def load_config(self):
        with open("config.json", "r", encoding="utf-8") as config_file:
            self.config = json.load(config_file)

    def get_info_from_text(self, text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        word_info = {}
        counter = Counter(token.text for token in doc if token.is_alpha)

        for token in doc:
            if not token.is_alpha:
                continue
            if token.text in word_info:
                continue

            morph_info = []
            if token.pos_:
                morph_info.append(f"Часть речи: {self.pos_map.get(token.pos_, token.pos_)}")
            if token.morph.get("Gender"):
                genders = [self.gender_map.get(g, g) for g in token.morph.get("Gender")]
                morph_info.append(f"Род: {', '.join(genders)}")
            if token.morph.get("Number"):
                numbers = [self.number_map.get(n, n) for n in token.morph.get("Number")]
                morph_info.append(f"Число: {', '.join(numbers)}")
            if token.morph.get("Case"):
                cases = [self.case_map.get(c, c) for c in token.morph.get("Case")]
                morph_info.append(f"Падеж: {', '.join(cases)}")

            morph_info_str = "\n".join(morph_info) if morph_info else "Нет данных"

            word_info[token.text] = (token.text, token.lemma_, counter[token.text], morph_info_str)

        return list(word_info.values())

    def is_russian(self, word):
        return bool(re.fullmatch(r"[а-яА-ЯёЁ]+", word))

def process_files(input_dir, output_dir, data_extractor):
    # Получаем все файлы из директории
    files = glob(os.path.join(input_dir, "*.txt"))

    # Регулярное выражение для разделения на предложения
    sentence_splitter = re.compile(r'(?<=[.!?])\s+(?=[А-ЯA-Z])')

    for file_path in files:
        # Читаем текст из файла
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read().strip()

        # Удаляем пустые строки
        text = "\n".join(line for line in text.split("\n") if line.strip())

        # Получаем информацию о словах
        word_info = data_extractor.get_info_from_text(text)

        # Создаем XML структуру
        root = ET.Element("root")
        file_name = os.path.basename(file_path)
        root.set("file", file_name)

        # Разбиваем текст на предложения
        sentences = sentence_splitter.split(text)

        for sentence_id, sentence in enumerate(sentences, start=1):
            sentence = sentence.strip()
            if not sentence:
                continue

            # Создаем элемент предложения в XML
            sentence_elem = ET.SubElement(root, "sentence", id=str(sentence_id))
            full_sentence_elem = ET.SubElement(sentence_elem, "full_sentence")
            full_sentence_elem.text = sentence

            # Извлекаем все слова из текущего предложения
            words_in_sentence = re.findall(r'\b\w+\b', sentence)

            # Для каждого слова из предложения находим информацию
            word_info_in_sentence = [
                info for info in word_info if info[0] in words_in_sentence
            ]

            # Добавляем каждое слово как элемент в XML
            for word_id, (word, lemma, count, morph_info) in enumerate(word_info_in_sentence, start=1):
                word_elem = ET.SubElement(
                    sentence_elem, "word", id=str(word_id), info=morph_info
                )
                word_elem.text = word

        # Сохраняем XML в файл
        os.makedirs(output_dir, exist_ok=True)
        output_file_path = os.path.join(output_dir, file_name.replace(".txt", ".xml"))
        tree = ET.ElementTree(root)
        tree.write(output_file_path, encoding="utf-8", xml_declaration=True)


# Функция для замера времени выполнения
def measure_time_for_files(input_dir, output_dir, data_extractor, num_files_list):
    times = []

    for num_files in num_files_list:
        # Выбираем первые num_files файлов
        files = glob(os.path.join(input_dir, "*.txt"))[:num_files]

        start_time = time.time()  # Начало замера времени

        # Процессинг файлов
        process_files(files, output_dir, data_extractor)

        end_time = time.time()  # Конец замера времени
        elapsed_time = end_time - start_time  # Время выполнения
        times.append(elapsed_time)

        print(f"Время для {num_files} файлов: {elapsed_time:.4f} секунд")

    return times

