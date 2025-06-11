import re
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import ttk, filedialog, messagebox

import nltk
from pymorphy3 import MorphAnalyzer
from ruwordnet import RuWordNet
from wiki_ru_wordnet import WikiWordnet


class SentencesWindow:
    def __init__(self, root, text):
        self.wikiwordnet = WikiWordnet()
        self.wn = RuWordNet()
        self.morph = MorphAnalyzer()
        self.text = text
        self.sentences = []
        self.last_parsed_tree = None
        self.window = tk.Toplevel(root)
        self.window.title("Предложения")
        self.setup_ui()
        nltk.download('punkt')
        nltk.download('punkt_tab')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger_rus')

    def setup_ui(self):
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        table_frame = tk.Frame(main_frame)
        table_frame.pack(side="left", fill="both", expand=True)

        filter_frame = tk.Frame(table_frame)
        filter_frame.pack(fill="x", pady=(0, 5))

        tk.Label(filter_frame, text="Поиск:").pack(side="left", padx=(0, 5))
        self.filter_entry = tk.Entry(filter_frame, width=40)
        self.filter_entry.pack(side="left")

        tk.Button(filter_frame, text="Применить", command=self.apply_filter).pack(side="left", padx=5)
        tk.Button(filter_frame, text="Сбросить", command=self.reset_filter).pack(side="left")
        tk.Button(filter_frame, text="Загрузить TXT", command=self.load_text_file).pack(side="left", padx=5)

        style = ttk.Style()
        style.configure("Treeview", rowheight=30)

        columns = ("sentence",)
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        self.tree.heading("sentence", text="Предложение")
        self.tree.column("sentence", width=800, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(expand=True, fill="both")

        self.sentences = self.split_into_sentences(self.text)
        self.display_sentences(self.sentences)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="y", padx=10)

        self.setup_controls(right_frame)

    def load_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.text = f.read()
                self.sentences = self.split_into_sentences(self.text)
                self.display_sentences(self.sentences)

    def setup_controls(self, right_frame):
        analysis_frame = ttk.LabelFrame(right_frame, text="Анализ", padding=10)
        analysis_frame.pack(fill="x", pady=(0, 10))

        semantic_btn = ttk.Button(analysis_frame, text="Семантический анализ", command=self.semantic_analysis)
        semantic_btn.pack(side="top", fill="x", pady=5)

        help_button = ttk.Button(analysis_frame, text="Помощь", command=self.show_help)
        help_button.pack(side="top", fill="x", pady=5)

        save_button = ttk.Button(analysis_frame, text="Сохранить семантический анализ", command=self.save_semantic_analysis)
        save_button.pack(side="top", fill="x", pady=5)

    def show_help(self):
        help_window = tk.Toplevel(self.window)
        help_window.title("Помощь")
        help_window.geometry("600x400")
        help_window.resizable(False, False)

        help_text = (
            "Как пользоваться этим окном:\n\n"
            "1. В таблице отображаются предложения из текста.\n"
            "2. Используйте поле 'Поиск', чтобы отфильтровать предложения по ключевым словам.\n"
            "3. Кнопка 'Применить' — применяет фильтр.\n"
            "4. Кнопка 'Сбросить' — сбрасывает фильтр и показывает все предложения.\n"
            "5. Выберите предложение в таблице:\n"
            "   - Нажмите 'Синтаксический анализ' — откроется дерево разбора предложения.\n"
            "   - Нажмите 'Семантический анализ' — появится информация из анализа текста.\n"
            "6. Кнопка 'Помощь' — открывает это окно помощи.\n"
            "7. Кнопка 'Применить свою грамматику' - откроется дерево разбора предложения с грамматикой указанной пользователем\n"
            "   - Выберите предложения в таблице\n"
            "   - Введите грамматику в поле ввода над кнопкой\n"
            "\nЕсли у вас возникли вопросы, обратитесь к разработчику: @dezzzll @babebrik"
        )

        help_label = tk.Label(help_window, text=help_text, justify="left", wraplength=580, padx=10, pady=10)
        help_label.pack(expand=True, fill="both")

        close_button = tk.Button(help_window, text="Закрыть", command=help_window.destroy)
        close_button.pack(pady=10)

    def split_into_sentences(self, text):
        return re.split(r'(?<=[.!?])\s+', text.strip())

    def display_sentences(self, sentences):
        self.tree.delete(*self.tree.get_children())
        for s in sentences:
            self.tree.insert("", "end", values=(s.strip(),))

    def apply_filter(self):
        filter_text = self.filter_entry.get().strip().lower()
        if not filter_text:
            return

        filtered = [s for s in self.sentences if filter_text in s.lower()]
        self.display_sentences(filtered)

    def reset_filter(self):
        self.filter_entry.delete(0, tk.END)
        self.display_sentences(self.sentences)

    def show_semantic_result(self, result):
        result_window = tk.Toplevel(self.window)
        result_window.title("Семантический анализ")
        result_window.geometry("700x500")

        text_box = tk.Text(result_window, wrap="word")
        text_box.insert("1.0", result)
        text_box.config(state="disabled")
        text_box.pack(expand=True, fill="both", padx=10, pady=10)

        close_btn = tk.Button(result_window, text="Закрыть", command=result_window.destroy)
        close_btn.pack(pady=10)

    def get_synonyms_from_ruwordnet(self, word):
        synonyms = set()
        synsets_ru = self.wn.get_synsets(word)
        for synset in synsets_ru:
            if synset.title.lower() != word.lower():
                synonyms.add(synset.title.lower())

        # wikiwordnet
        synsets_wiki = self.wikiwordnet.get_synsets(word)
        for synset in synsets_wiki:
            for lemma in synset.get_words():
                if lemma.lemma() != word:
                    synonyms.add(lemma.lemma())
        return ', '.join(synonyms) if synonyms else '—'

    def get_hypernyms_from_wikiwordnet(self, word):
        synsets = self.wikiwordnet.get_synsets(word)
        hypernyms = set()
        if synsets:
            synset = synsets[0]
            for hypernym in self.wikiwordnet.get_hypernyms(synset):
                for w in hypernym.get_words():
                    hypernyms.add(w.lemma())
        synsets = self.wn.get_senses(word)
        for synset in synsets:
            for hypernym in synset.synset.hypernyms:
                hypernyms.add(hypernym.definition)
        return ', '.join(hypernyms) if hypernyms else '—'

    def get_antonyms_from_wikiwordnet(self, word):
        antonyms = set()
        synsets = self.wn.get_senses(word)
        for synset in synsets:
            for antonym in synset.synset.antonyms:
                antonyms.add(antonym.definition)
        return ', '.join(antonyms) if antonyms else '—'

    def get_hyponyms_from_wikiwordnet(self, word):
        synsets = self.wikiwordnet.get_synsets(word)
        if not synsets:
            return '—'
        synset = synsets[0]
        hyponyms = set()
        for hyponym in self.wikiwordnet.get_hyponyms(synset):
            for w in hyponym.get_words():
                hyponyms.add(w.lemma())
        synsets = self.wn.get_senses(word)
        for synset in synsets:
            for hyponym in synset.synset.hyponyms:
                hyponyms.add(hyponym.definition)
        return ', '.join(hyponyms) if hyponyms else '—'

    def get_definition_from_wikiwordnet(self, word):
        synsets = self.wikiwordnet.get_synsets(word)
        if not synsets:
            return '—'
        synset = synsets[0]
        definitions = {w.definition() for w in synset.get_words()}
        return '; '.join(definitions) if definitions else '—'

    def create_semantic_xml(self, sentence):
        root = ET.Element("SemanticAnalysis")
        root.set("sentence", sentence)

        words = nltk.word_tokenize(sentence, language='russian')

        for word in words:
            parsed = self.morph.parse(word)[0]
            pos = parsed.tag.POS

            if pos in {'PREP', 'CONJ', 'PRCL', 'INTJ', 'None', 'ADVB', 'ADJF'}:
                continue

            lemma = parsed.normal_form

            if self.wikiwordnet.get_synsets(lemma):
                word_elem = ET.SubElement(root, "Word")
                ET.SubElement(word_elem, "Original").text = word
                ET.SubElement(word_elem, "Lemma").text = lemma
                ET.SubElement(word_elem, "POS").text = pos

                ET.SubElement(word_elem, "Synonyms").text = self.get_synonyms_from_ruwordnet(lemma)
                ET.SubElement(word_elem, "Hypernyms").text = self.get_hypernyms_from_wikiwordnet(lemma)
                ET.SubElement(word_elem, "Hyponyms").text = self.get_hyponyms_from_wikiwordnet(lemma)
                ET.SubElement(word_elem, "Definition").text = self.get_definition_from_wikiwordnet(lemma)

        self.semantic_xml = ET.ElementTree(root)

    def semantic_analysis(self):
        selected = self.tree.selection()
        if not selected:
            return

        sentence = self.tree.item(selected[0])["values"][0]
        words = nltk.word_tokenize(sentence, language='russian')
        result_output = ""

        for word in words:
            parsed = self.morph.parse(word)[0]
            pos = parsed.tag.POS

            if pos in {'PREP', 'CONJ', 'PRCL', 'INTJ', 'None', 'ADVB', 'ADJF'}:
                continue

            lemma = parsed.normal_form

            # Только если есть синсеты в wikiwordnet
            if self.wikiwordnet.get_synsets(lemma):
                synonyms = self.get_synonyms_from_ruwordnet(lemma)
                hypernyms = self.get_hypernyms_from_wikiwordnet(lemma)
                hyponyms = self.get_hyponyms_from_wikiwordnet(lemma)
                definition = self.get_definition_from_wikiwordnet(lemma)

                result_output += f"🔹 Слово: {word} | Лемма: {lemma} | POS: {pos}\n"
                result_output += f"   🔸 Синонимы: {synonyms}\n"
                result_output += f"   🔸 Гиперонимы: {hypernyms}\n"
                result_output += f"   🔸 Гипонимы: {hyponyms}\n"
                result_output += f"   🔸 Описание: {definition}\n"
                result_output += "-------------------------------------------------\n"

        self.create_semantic_xml(sentence)
        self.show_semantic_result(result_output)

    def save_semantic_analysis(self):
        if not hasattr(self, "semantic_xml") or self.semantic_xml is None:
            messagebox.showwarning("Предупреждение",
                                   "Нет семантического разбора для сохранения. Сначала выполните анализ.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xml",
                                                 filetypes=[("XML files", "*.xml")])
        if file_path:
            self.semantic_xml.write(file_path, encoding="utf-8", xml_declaration=True)
            messagebox.showinfo("Успех", f"Семантический разбор сохранён в файл:\n{file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    text = ""
    app = SentencesWindow(root, text)
    root.mainloop()