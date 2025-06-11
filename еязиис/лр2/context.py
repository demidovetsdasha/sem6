import os
import re
import xml.etree.ElementTree as ET
from glob import glob

import os
import xml.etree.ElementTree as ET
from glob import glob


def find_sentences_with_word(phrase, count=None, xml_dir="corpus_xml"):
    # xml_dir = "corpus_xml"
    found_sentences = []

    # Получаем все XML-файлы
    xml_files = glob(os.path.join(xml_dir, "*.xml"))

    # Создаем регулярное выражение для поиска целых слов или точных фраз
    phrase_pattern = r'\b' + re.escape(phrase) + r'\b'

    for file_path in xml_files:
        tree = ET.parse(file_path)
        root = tree.getroot()

        rating = root.find("meta/rating")
        rating_text = rating.text if rating is not None else "Рейтинг не указан"

        filename = os.path.basename(file_path)  # Название файла

        for sentence in root.findall("sentence"):
            full_sentence_elem = sentence.find("full_sentence")

            if full_sentence_elem is not None:
                full_sentence = full_sentence_elem.text

                # Проверяем, есть ли фраза как отдельное слово или точное совпадение фразы
                if re.search(phrase_pattern, full_sentence):
                    found_sentences.append((full_sentence, rating_text, filename))

            # Ограничение количества найденных предложений
            if count is not None and len(found_sentences) >= count:
                return found_sentences

    return found_sentences


