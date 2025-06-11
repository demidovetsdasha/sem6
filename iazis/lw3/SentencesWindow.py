import json
import re
import string
import tkinter as tk
import time
from tkinter import ttk, messagebox, filedialog
from unittest.mock import MagicMock

import xml.etree.ElementTree as ET
import nltk
from nltk import pos_tag, word_tokenize, RegexpParser
from nltk.draw import TreeWidget
from nltk.draw.util import CanvasFrame


class SentencesWindow:
    def __init__(self, root, text):
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

        syntax_button = ttk.Button(analysis_frame, text="Синтаксический анализ", command=self.syntax_analysis)
        syntax_button.pack(side="top", fill="x", pady=5)

        ttk.Label(analysis_frame, text="Своя грамматика:").pack(fill="x")
        self.grammar_text = tk.Text(analysis_frame, height=8, width=40)
        self.grammar_text.pack(fill="x", pady=5)

        custom_button = ttk.Button(analysis_frame, text="Применить свою грамматику",
                                   command=self.syntax_analysis_custom)
        custom_button.pack(side="top", fill="x", pady=5)

        help_button = ttk.Button(analysis_frame, text="Помощь", command=self.show_help)
        help_button.pack(side="top", fill="x", pady=5)

        save_button = ttk.Button(analysis_frame, text="Сохранить дерево в XML", command=self.save_current_tree_as_xml)
        save_button.pack(side="top", fill="x", pady=5)

    def syntax_analysis_custom(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите предложение для анализа.")
            return

        grammar_input = self.grammar_text.get("1.0", "end").strip()
        if not grammar_input:
            messagebox.showwarning("Предупреждение", "Введите правила грамматики.")
            return

        sentence = self.tree.item(selected_item)["values"][0]
        self.show_syntax_tree(sentence, grammar_input)

    def syntax_analysis(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите предложение для анализа.")
            return

        sentence = self.tree.item(selected_item)["values"][0]
        self.show_syntax_tree(sentence)

    def show_syntax_tree(self, sentence: str, grammar_text: str = None):
        if grammar_text is None:
            grammar_text = """
            NP: {<S-PRO>?<A-PRO.*>*<A=.*>*<S>}
            P: {<PR>}
            V: {<PART>?<V.*>}
            PP: {<P> <NP>}
            VP: {<V> <NP|PP>*}
            SC: {<NP> <VP>}
            """

        try:
            grammar = RegexpParser(grammar_text)
        except Exception as e:
            messagebox.showerror("Ошибка грамматики", f"Ошибка в правилах грамматики:\n{str(e)}")
            return

        try:
            tagged = pos_tag(
                [word for word in word_tokenize(sentence) if word not in string.punctuation],
                lang="rus"
            )

            output = grammar.parse(tagged)
            self.last_parsed_tree = output

            canvas_frame = CanvasFrame(width=1500, height=500)
            tree = TreeWidget(canvas_frame.canvas(), output)
            canvas_frame.add_widget(tree, 10, 10)
            canvas_frame.mainloop()

            def tree_to_xml(node):
                if isinstance(node, tuple):
                    el = ET.Element("word")
                    el.set("text", node[0])
                    el.set("tag", node[1])
                    return el
                else:
                    el = ET.Element(node.label())
                    for child in node:
                        el.append(tree_to_xml(child))
                    return el

            root_element = tree_to_xml(output)
            tree = ET.ElementTree(root_element)
            xml_filename = f"tree_{int(time.time())}.xml"
            tree.write(xml_filename, encoding="utf-8", xml_declaration=True)

        except Exception as e:
            messagebox.showerror("Ошибка анализа", f"Ошибка при разборе предложения:\n{str(e)}")

    def semantic_analysis(self):
        print("Семантический анализ:")
        print(self.analysis_result)

    def save_current_tree_as_xml(self):
        if self.last_parsed_tree is None:
            messagebox.showwarning("Предупреждение",
                                   "Нет дерева для сохранения. Сначала выполните синтаксический анализ.")
            return

        def tree_to_xml(node):
            if isinstance(node, tuple):  # Лист
                el = ET.Element("word")
                el.set("text", node[0])
                el.set("tag", node[1])
                return el
            else:
                el = ET.Element(node.label())
                for child in node:
                    el.append(tree_to_xml(child))
                return el

        root_element = tree_to_xml(self.last_parsed_tree)
        tree = ET.ElementTree(root_element)

        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if file_path:
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
            messagebox.showinfo("Успех", f"Сохранено в файл:\n{file_path}")

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

def test_syntax_tree_performance():
    text = (
        "Мама мыла раму. Папа читал газету. Дети играли во дворе. "
        "Кошка спала на подоконнике. Солнце светило ярко. "
        "Птицы пели в саду. Машина проехала мимо. Дождь пошел внезапно. "
        "Зонта не было. Люди бежали по улице. Все промокли до нитки."
    )

    root = tk.Tk()
    root.withdraw()

    app = SentencesWindow(root, text)

    app.show_syntax_tree = MagicMock(side_effect=app.show_syntax_tree)

    for i in range(1, 11):
        sentences_subset = app.sentences[:i]
        start_time = time.time()
        for sentence in sentences_subset:
            app.show_syntax_tree(sentence)
        elapsed_time = time.time() - start_time
        print(f"Время анализа для {i} предложений: {elapsed_time:.4f} секунд")

    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    text = ""

    app = SentencesWindow(root, text)

    root.mainloop()
