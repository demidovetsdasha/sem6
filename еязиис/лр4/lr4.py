import re
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import ttk, filedialog, messagebox, scrolledtext
from dataclasses import dataclass, field
import csv

import requests
from pdfminer.high_level import extract_text
from typing import List, Optional
from pymorphy3 import MorphAnalyzer
import nltk
import spacy
from ruwordnet import RuWordNet
from wiki_ru_wordnet import WikiWordnet
from bs4 import BeautifulSoup

nltk.download('punkt')
nltk.download('omw-1.4')

morph = MorphAnalyzer()
wn = RuWordNet()
wikiwordnet = WikiWordnet()

try:
    nlp = spacy.load("ru_core_news_sm")
except OSError:
    messagebox.showerror("Ошибка", "Установите модель: python -m spacy download ru_core_news_sm")
    exit()

@dataclass
class TreeNode:
    label: str
    text: str = ""
    children: List['TreeNode'] = field(default_factory=list)
    x: int = 0
    y: int = 0
    width: int = 80
    height: int = 40
    canvas_id: int = None
    text_id: int = None

@dataclass
class SentenceData:
    text: str
    tokens: list
    semantic_analysis: list = field(default_factory=list)
    tree_root: Optional[TreeNode] = None
    subjects: list = field(default_factory=list)
    predicates: list = field(default_factory=list)
    objects: list = field(default_factory=list)
    attributes: list = field(default_factory=list)
    adverbials: list = field(default_factory=list)

class SyntaxApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Синтаксический и семантический анализ")
        self.geometry("1200x800")
        self.sentences = []
        self.filtered_sentences = []
        self.current_file = ""
        self.dragged_node = None
        self.start_x = 0
        self.start_y = 0
        self.semantic_xml = None
        self.create_menu()
        self.create_widgets()
        self.create_help_tab()

    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Открыть PDF", command=self.load_file)
        file_menu.add_command(label="Сохранить XML", command=self.save_semantic_analysis)
        file_menu.add_command(label="Сохранить TXT", command=self.save_result_txt)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        analysis_menu = tk.Menu(menubar, tearoff=0)
        analysis_menu.add_command(label="Статистика", command=self.show_members_stats)
        analysis_menu.add_command(label="Поиск по членам", command=self.find_by_members_dialog)
        analysis_menu.add_command(label="Сохранить сем. анализ", command=self.save_semantic_analysis)
        menubar.add_cascade(label="Анализ", menu=analysis_menu)
        menubar.add_command(label="Справка", command=self.show_help)
        self.config(menu=menubar)

    def create_widgets(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        filter_frame = tk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        tk.Label(filter_frame, text="Фильтр:").pack(side=tk.LEFT, padx=5)
        self.sentence_filter_entry = tk.Entry(filter_frame, width=50)
        self.sentence_filter_entry.pack(side=tk.LEFT, padx=5)
        self.sentence_filter_entry.bind("<KeyRelease>", lambda e: self.auto_filter())
        display_frame = tk.Frame(main_frame)
        display_frame.pack(fill=tk.BOTH, expand=True)
        table_frame = tk.Frame(display_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        columns = ("text", "subjects", "predicates", "objects", "attributes", "adverbials")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                 yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set, height=15)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100 if col != "text" else 300)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        self.notebook = ttk.Notebook(display_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        semantic_frame = tk.Frame(self.notebook)
        self.semantic_text = scrolledtext.ScrolledText(semantic_frame, wrap=tk.WORD, height=10)
        self.semantic_text.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(semantic_frame, text="Семантика")
        members_frame = tk.Frame(self.notebook)
        self.members_text = scrolledtext.ScrolledText(members_frame, wrap=tk.WORD, height=10)
        self.members_text.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(members_frame, text="Синтаксис")
        tokens_frame = tk.Frame(self.notebook)
        self.tokens_text = scrolledtext.ScrolledText(tokens_frame, wrap=tk.WORD, height=10)
        self.tokens_text.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(tokens_frame, text="Токены")
        tree_frame = tk.Frame(self.notebook)
        canvas_scroll_y = ttk.Scrollbar(tree_frame)
        canvas_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        canvas_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        canvas_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_canvas = tk.Canvas(tree_frame, bg='white', yscrollcommand=canvas_scroll_y.set,
                                     xscrollcommand=canvas_scroll_x.set)
        self.tree_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas_scroll_y.config(command=self.tree_canvas.yview)
        canvas_scroll_x.config(command=self.tree_canvas.xview)
        self.tree_canvas.bind("<Button-1>", self.on_node_click)
        self.tree_canvas.bind("<B1-Motion>", self.on_node_drag)
        self.tree_canvas.bind("<ButtonRelease-1>", self.on_node_release)
        self.tree_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.tree_canvas.bind("<Shift-MouseWheel>", self._on_shift_mousewheel)
        self.notebook.add(tree_frame, text="Дерево")
        self.tree.bind("<<TreeviewSelect>>", self.show_sentence_details)
        self.tree.bind("<Double-1>", self.edit_sentence)
        self.status_bar = tk.Label(self, text="Готово", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X)

    def _on_mousewheel(self, event):
        self.tree_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_shift_mousewheel(self, event):
        self.tree_canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def create_help_tab(self):
        help_frame = tk.Frame(self.notebook)
        help_text = scrolledtext.ScrolledText(help_frame, wrap=tk.WORD, height=10)
        help_text.pack(fill=tk.BOTH, expand=True)
        help_content = """Инструкция:
1. Откройте PDF-файл через меню Файл -> Открыть PDF
2. Выберите предложение в таблице для просмотра анализа
3. Используйте вкладки для просмотра разных видов анализа
4. Редактируйте предложения двойным кликом
5. Сохраняйте результаты в XML или TXT"""
        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)
        self.notebook.add(help_frame, text="Справка")

    def get_synonyms(self, word):
        synonyms = set()
        synsets_ru = wn.get_synsets(word)
        for synset in synsets_ru:
            if synset.title.lower() != word.lower():
                synonyms.add(synset.title.lower())
        synsets_wiki = wikiwordnet.get_synsets(word)
        for synset in synsets_wiki:
            for lemma in synset.get_words():
                if lemma.lemma() != word:
                    synonyms.add(lemma.lemma())
        return ', '.join(synonyms) if synonyms else '—'

    def get_hypernyms(self, word):
        synsets = wikiwordnet.get_synsets(word)
        hypernyms = set()
        if synsets:
            synset = synsets[0]
            for hypernym in wikiwordnet.get_hypernyms(synset):
                for w in hypernym.get_words():
                    hypernyms.add(w.lemma())
        synsets = wn.get_senses(word)
        for synset in synsets:
            for hypernym in synset.synset.hypernyms:
                hypernyms.add(hypernym.definition)
        return ', '.join(hypernyms) if hypernyms else '—'

    def get_hyponyms(self, word):
        synsets = wikiwordnet.get_synsets(word)
        if not synsets:
            return '—'
        synset = synsets[0]
        hyponyms = set()
        for hyponym in wikiwordnet.get_hyponyms(synset):
            for w in hyponym.get_words():
                hyponyms.add(w.lemma())
        synsets = wn.get_senses(word)
        for synset in synsets:
            for hyponym in synset.synset.hyponyms:
                hyponyms.add(hyponym.definition)
        return ', '.join(hyponyms) if hyponyms else '—'


    
    def create_semantic_xml(self):
        # Создаем корневой элемент для всего документа
        root = ET.Element("SemanticAnalysisDocument")

        for sent in self.sentences:
            sentence_elem = ET.SubElement(root, "Sentence")
            sentence_elem.set("text", sent.text.strip())

            # Обрабатываем слова с семантической информацией
            for word_info in getattr(sent, "semantic_analysis", []):
                if not any([word_info.get('synonyms'), word_info.get('hypernyms'), word_info.get('hyponyms')]):
                    continue

                word_elem = ET.SubElement(sentence_elem, "Word")
                ET.SubElement(word_elem, "Original").text = word_info.get("word", "")
                ET.SubElement(word_elem, "POS").text = word_info.get("POS", "")
                ET.SubElement(word_elem, "Description").text = ', '.join(word_info.get("definition", []))
                ET.SubElement(word_elem, "Synonyms").text = ', '.join(word_info.get("synonyms", []))
                ET.SubElement(word_elem, "Hypernyms").text = ', '.join(word_info.get("hypernyms", []))
                ET.SubElement(word_elem, "Hyponyms").text = ', '.join(word_info.get("hyponyms", []))

        self.semantic_xml = ET.ElementTree(root)


    def save_semantic_analysis(self):
        if not self.sentences:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения")
            return

        try:
            # Генерируем XML-структуру
            self.create_semantic_xml()

            file_path = filedialog.asksaveasfilename(
                defaultextension=".xml",
                filetypes=[("XML files", "*.xml")]
            )

            if not file_path:
                return

            # Сохраняем файл
            self.semantic_xml.write(file_path, encoding="utf-8", xml_declaration=True)
            messagebox.showinfo("Успех", f"Файл сохранен:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")

    def find_local_examples(self, word, sentences):
        examples = []
        lemma = morph.parse(word)[0].normal_form
        for sent in sentences:
            if lemma in sent.text.lower():
                examples.append(sent.text)
                if len(examples) >= 3:
                    break
        return examples

    def get_definition(self, word: str) -> str:
        synsets = wikiwordnet.get_synsets(word)
        if not synsets:
            return '—'
        synset = synsets[0]
        definitions = {w.definition() for w in synset.get_words()}
        return '; '.join(definitions) if definitions else '—'

    def get_semantic_info(self, word: str) -> dict:
        # Пропуск пунктуации и пробелов
        if any(c in r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ """ for c in word):
            return {
                'word': word,
                'POS': 'PUNCT/SPACE',
                'definition': '—',
                'synonyms': [],
                'hypernyms': [],
                'hyponyms': [],
                #'antonyms': [],
                'examples': []
            }

        doc = nlp(word)
        parsed = morph.parse(word)[0]
        base_form = parsed.normal_form.lower()
        spacy_pos = doc[0].pos_

        result = {
            'word': word,
            'POS': spacy_pos,
            'definition': self.get_definition(base_form),
            'synonyms': self.get_synonyms(base_form).split(', '),
            'hypernyms': self.get_hypernyms(base_form).split(', '),
            'hyponyms': self.get_hyponyms(base_form).split(', '),
            #'antonyms': self.get_antonyms(base_form).split(', '),
            'examples': self.find_local_examples(base_form, self.sentences)
        }
        return result

    def build_syntax_tree(self, sent):
        tokens = list(sent)
        if not tokens: return None
        root = TreeNode(label="S")
        current_vp = None
        current_np = None
        current_pp = None
        for token in tokens:
            if token.pos_ == "VERB" or token.dep_ == "ROOT":
                current_vp = TreeNode(label="VP")
                current_vp.children.append(TreeNode(label="VERB", text=token.text))
                root.children.append(current_vp)
            elif token.pos_ == "NOUN":
                current_np = TreeNode(label="NP")
                current_np.children.append(TreeNode(label="NOUN", text=token.text))
                if current_vp: current_vp.children.append(current_np)
                else: root.children.append(current_np)
            elif token.pos_ == "ADJ":
                adj_node = TreeNode(label="ADJECTIVE", text=token.text)
                if current_np: current_np.children.append(adj_node)
            elif token.pos_ == "ADP":
                current_pp = TreeNode(label="PP")
                current_pp.children.append(TreeNode(label="PREPOSITION", text=token.text))
                if current_np: current_np.children.append(current_pp)
            elif token.pos_ == "PROPN":
                propn_node = TreeNode(label="NOUN", text=token.text)
                if current_pp: current_pp.children.append(propn_node)
                elif current_np: current_np.children.append(propn_node)
        return root

    def draw_syntax_tree(self, root):
        self.tree_canvas.delete("all")
        if not root: return
        self.calculate_node_positions(root, self.tree_canvas.winfo_width()//2, 50, 200)
        self.update_canvas_scroll_region(root)
        self.draw_tree_connections(root)
        self.draw_tree_nodes(root)

    def calculate_node_positions(self, node, x, y, x_step):
        node.x = x
        node.y = y
        if not node.children: return
        total_width = len(node.children)*x_step
        start_x = x - total_width//2 + x_step//2
        for i, child in enumerate(node.children):
            child_x = start_x + i*x_step
            self.calculate_node_positions(child, child_x, y+100, x_step*0.7)

    def draw_tree_connections(self, node):
        for child in node.children:
            self.tree_canvas.create_line(node.x, node.y+node.height//2, child.x, child.y-child.height//2, fill="black", width=1)
            self.draw_tree_connections(child)

    def draw_tree_nodes(self, node):
        node.canvas_id = self.tree_canvas.create_rectangle(
            node.x-node.width//2, node.y-node.height//2,
            node.x+node.width//2, node.y+node.height//2,
            fill="lightgray", outline="black", tags="node")
        text = f"{node.label}\n{node.text}" if node.text else node.label
        node.text_id = self.tree_canvas.create_text(node.x, node.y, text=text, font=("Arial",10), tags="node_text")
        for child in node.children: self.draw_tree_nodes(child)

    def update_canvas_scroll_region(self, root):
        min_x = max_x = root.x
        min_y = max_y = root.y
        def traverse(node):
            nonlocal min_x, max_x, min_y, max_y
            min_x = min(min_x, node.x-node.width//2)
            max_x = max(max_x, node.x+node.width//2)
            min_y = min(min_y, node.y-node.height//2)
            max_y = max(max_y, node.y+node.height//2)
            for child in node.children: traverse(child)
        traverse(root)
        self.tree_canvas.config(scrollregion=(min_x-100, min_y-100, max_x+100, max_y+100))

    def on_node_click(self, event):
        closest = self.tree_canvas.find_closest(event.x, event.y)
        if not closest: return
        item = closest[0]
        tags = self.tree_canvas.gettags(item)
        if "node" in tags or "node_text" in tags:
            if "node_text" in tags:
                for obj in self.tree_canvas.find_all():
                    if "node" in self.tree_canvas.gettags(obj) and self.tree_canvas.coords(obj)[0] <= event.x <= self.tree_canvas.coords(obj)[2]:
                        item = obj
                        break
            selected_item = item
            self.dragged_node = self.find_node_by_canvas_id(self.get_selected_sentence().tree_root, selected_item)
            if self.dragged_node:
                self.start_x = event.x
                self.start_y = event.y

    def on_node_drag(self, event):
        if self.dragged_node:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.dragged_node.x += dx
            self.dragged_node.y += dy
            self.tree_canvas.move(self.dragged_node.canvas_id, dx, dy)
            self.tree_canvas.move(self.dragged_node.text_id, dx, dy)
            self.redraw_connections_for_node(self.dragged_node)
            self.start_x = event.x
            self.start_y = event.y

    def on_node_release(self, event):
        self.dragged_node = None

    def find_node_by_canvas_id(self, node, canvas_id):
        if node.canvas_id == canvas_id: return node
        for child in node.children:
            found = self.find_node_by_canvas_id(child, canvas_id)
            if found: return found
        return None

    def redraw_connections_for_node(self, node):
        for item in self.tree_canvas.find_all():
            if "line" in self.tree_canvas.gettags(item) or "line_text" in self.tree_canvas.gettags(item):
                self.tree_canvas.delete(item)
        self.draw_tree_connections(self.get_selected_sentence().tree_root)

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Выберите PDF", filetypes=[("PDF files", "*.pdf")])
        if not file_path: return
        try:
            text = extract_text(file_path)
            if not text.strip():
                messagebox.showerror("Ошибка", "Не удалось извлечь текст")
                return
            self.current_file = file_path
            self.status_bar.config(text=f"Обработка: {file_path}...")
            self.update()
            doc = nlp(text)
            self.sentences = []
            for sent in doc.sents:
                tokens_info = []
                semantic_info = []
                subjects = []
                predicates = []
                objects = []
                attributes = []
                adverbials = []
                for token in sent:
                    if token.is_space or token.is_punct:
                        continue

                    tokens_info.append(f"{token.text} ({token.pos_}) -> {token.dep_} -> {token.head.text}")
                    semantic_info.append(self.get_semantic_info(token.text))
                    if token.dep_ in ["nsubj", "nsubj:pass"]:
                        subjects.append(token.text)
                    elif token.pos_ == "VERB" or token.dep_ == "ROOT":
                        predicates.append(token.text)
                    elif token.dep_ in ["obj", "iobj", "obl"]:
                        objects.append(token.text)
                    elif token.dep_ in ["amod", "nummod"]:
                        attributes.append(token.text)
                    elif token.dep_ in ["advmod", "nmod"]:
                        adverbials.append(token.text)
                tree_root = self.build_syntax_tree(sent)
                self.sentences.append(SentenceData(
                    text=sent.text,
                    tokens=tokens_info,
                    semantic_analysis=semantic_info,
                    tree_root=tree_root,
                    subjects=subjects,
                    predicates=predicates,
                    objects=objects,
                    attributes=attributes,
                    adverbials=adverbials
                ))
            self.filtered_sentences = self.sentences.copy()
            self.refresh_treeview()
            self.status_bar.config(text=f"Готово: {len(self.sentences)} предложений")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обработки: {str(e)}")
            self.status_bar.config(text="Ошибка")

    def refresh_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for sent in self.filtered_sentences:
            short_text = (sent.text[:100]+'...') if len(sent.text)>100 else sent.text
            self.tree.insert("", tk.END, values=(
                short_text,
                ", ".join(sent.subjects) if sent.subjects else "-",
                ", ".join(sent.predicates) if sent.predicates else "-",
                ", ".join(sent.objects) if sent.objects else "-",
                ", ".join(sent.attributes) if sent.attributes else "-",
                ", ".join(sent.adverbials) if sent.adverbials else "-"
            ))

    def show_sentence_details(self, event):
        selected_item = self.tree.focus()
        if not selected_item: return
        idx = self.tree.index(selected_item)
        if 0 <= idx < len(self.filtered_sentences):
            sent = self.filtered_sentences[idx]
            self.members_text.config(state=tk.NORMAL)
            self.members_text.delete(1.0, tk.END)
            self.tokens_text.config(state=tk.NORMAL)
            self.tokens_text.delete(1.0, tk.END)
            self.semantic_text.config(state=tk.NORMAL)
            self.semantic_text.delete(1.0, tk.END)
            self.semantic_text.insert(tk.END, "Семантический анализ:\n\n")
            for word_info in sent.semantic_analysis:
                self.semantic_text.insert(tk.END,f"🔹 Слово: {word_info['word']} | POS: {word_info['POS']}\n")
                self.semantic_text.insert(tk.END, f"   Определение: {word_info['definition']}\n")
                self.semantic_text.insert(tk.END, f"   Синонимы: {', '.join(word_info['synonyms'][:5])}\n")
                self.semantic_text.insert(tk.END, f"   Гиперонимы: {', '.join(word_info['hypernyms'][:3])}\n")
                self.semantic_text.insert(tk.END, f"   Гипонимы: {', '.join(word_info['hyponyms'][:3])}\n")
                #self.semantic_text.insert(tk.END, f"   Антонимы: {', '.join(word_info['antonyms'][:3])}\n")
                self.semantic_text.insert(tk.END, "  Примеры использования:\n")
                for example in word_info['examples'][:3]:
                    self.semantic_text.insert(tk.END, f"      - {example}\n")
                self.semantic_text.insert(tk.END, "\n"+"-"*50+"\n\n")
            self.members_text.insert(tk.END, f"Предложение: {sent.text}\n\n")
            self.members_text.insert(tk.END, "Подлежащие:\n"+"\n".join(f"- {s}" for s in sent.subjects)+"\n\n")
            self.members_text.insert(tk.END, "Сказуемые:\n"+"\n".join(f"- {p}" for p in sent.predicates)+"\n\n")
            self.members_text.insert(tk.END, "Дополнения:\n"+"\n".join(f"- {o}" for o in sent.objects)+"\n\n")
            self.members_text.insert(tk.END, "Определения:\n"+"\n".join(f"- {a}" for a in sent.attributes)+"\n\n")
            self.members_text.insert(tk.END, "Обстоятельства:\n"+"\n".join(f"- {a}" for a in sent.adverbials)+"\n")
            self.tokens_text.insert(tk.END, "Токены:\n\n"+"\n".join(f"- {t}" for t in sent.tokens))
            self.draw_syntax_tree(sent.tree_root)
            self.members_text.config(state=tk.DISABLED)
            self.tokens_text.config(state=tk.DISABLED)
            self.semantic_text.config(state=tk.DISABLED)
            self.create_semantic_xml(sent.text)

    def get_selected_sentence(self):
        selected_item = self.tree.focus()
        if not selected_item: return None
        idx = self.tree.index(selected_item)
        if 0 <= idx < len(self.filtered_sentences): return self.filtered_sentences[idx]
        return None

    def show_members_stats(self):
        if not self.sentences:
            messagebox.showwarning("Предупреждение", "Нет данных")
            return
        stats_window = tk.Toplevel(self)
        stats_window.title("Статистика")
        stats_window.geometry("500x400")
        text = scrolledtext.ScrolledText(stats_window, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True)
        total = len(self.sentences)
        stats = {
            "Подлежащие": sum(len(s.subjects) for s in self.sentences),
            "Сказуемые": sum(len(s.predicates) for s in self.sentences),
            "Дополнения": sum(len(s.objects) for s in self.sentences),
            "Определения": sum(len(s.attributes) for s in self.sentences),
            "Обстоятельства": sum(len(s.adverbials) for s in self.sentences)
        }
        text.insert(tk.END, f"Статистика по {total} предложениям:\n\n")
        for k, v in stats.items():
            text.insert(tk.END, f"{k}: {v} (среднее: {v/total:.1f})\n")
        text.config(state=tk.DISABLED)

    def find_by_members_dialog(self):
        if not self.sentences:
            messagebox.showwarning("Предупреждение", "Нет данных")
            return
        dialog = tk.Toplevel(self)
        dialog.title("Поиск")
        dialog.geometry("400x300")
        tk.Label(dialog, text="Тип члена:").pack(pady=5)
        member_var = tk.StringVar()
        ttk.Combobox(dialog, textvariable=member_var,
                    values=["Подлежащее", "Сказуемое", "Дополнение", "Определение", "Обстоятельство"]).pack(pady=5)
        tk.Label(dialog, text="Текст:").pack(pady=5)
        text_entry = tk.Entry(dialog)
        text_entry.pack(pady=5)
        def search():
            member_type = member_var.get()
            text_query = text_entry.get().strip().lower()
            if not member_type:
                messagebox.showwarning("Ошибка", "Выберите тип")
                return
            member_map = {
                "Подлежащее": "subjects",
                "Сказуемое": "predicates",
                "Дополнение": "objects",
                "Определение": "attributes",
                "Обстоятельство": "adverbials"
            }
            member_field = member_map[member_type]
            found = []
            for sent in self.sentences:
                members = getattr(sent, member_field)
                if not text_query and members:
                    found.append(sent)
                else:
                    for m in members:
                        if text_query in m.lower():
                            found.append(sent)
                            break
            result_window = tk.Toplevel(dialog)
            result_window.title("Результаты")
            result_window.geometry("800x600")
            if not found:
                tk.Label(result_window, text="Не найдено").pack(pady=20)
                return
            text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD)
            text.pack(fill=tk.BOTH, expand=True)
            text.insert(tk.END, f"Найдено {len(found)} предложений:\n\n")
            for i, sent in enumerate(found, 1):
                text.insert(tk.END, f"{i}. {sent.text}\n{member_type}: {', '.join(getattr(sent, member_field))}\n\n")
            text.config(state=tk.DISABLED)
        tk.Button(dialog, text="Искать", command=search).pack(pady=10)

    def save_result_csv(self):
        if not self.sentences:
            messagebox.showwarning("Ошибка", "Нет данных")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path: return
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(
                    ["Предложение", "Подлежащие", "Сказуемые", "Дополнения", "Определения", "Обстоятельства"])
                for sent in self.sentences:
                    writer.writerow([
                        sent.text,
                        ", ".join(sent.subjects),
                        ", ".join(sent.predicates),
                        ", ".join(sent.objects),
                        ", ".join(sent.attributes),
                        ", ".join(sent.adverbials)
                    ])
            messagebox.showinfo("Успех", f"Сохранено в {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")

    def save_result_txt(self):
        if not self.sentences:
            messagebox.showwarning("Ошибка", "Нет данных")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not file_path: return
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Анализ файла: {self.current_file}\n")
                f.write(f"Всего предложений: {len(self.sentences)}\n\n")
                for i, sent in enumerate(self.sentences, 1):
                    f.write(f"Предложение {i}:\n{sent.text}\n")
                    f.write(f"Подлежащие: {', '.join(sent.subjects) if sent.subjects else 'Нет'}\n")
                    f.write(f"Сказуемые: {', '.join(sent.predicates) if sent.predicates else 'Нет'}\n")
                    f.write(f"Дополнения: {', '.join(sent.objects) if sent.objects else 'Нет'}\n")
                    f.write(f"Определения: {', '.join(sent.attributes) if sent.attributes else 'Нет'}\n")
                    f.write(f"Обстоятельства: {', '.join(sent.adverbials) if sent.adverbials else 'Нет'}\n")
                    f.write("\n"+"="*80+"\n\n")
                messagebox.showinfo("Успех", f"Сохранено в {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")

    def auto_filter(self):
        filter_text = self.sentence_filter_entry.get().lower()
        self.filtered_sentences = [sent for sent in self.sentences if filter_text in sent.text.lower()]
        self.refresh_treeview()

    def edit_sentence(self, event):
        selected_item = self.tree.focus()
        if not selected_item: return
        idx = self.tree.index(selected_item)
        if 0 <= idx < len(self.filtered_sentences):
            self.edit_sentence_dialog(self.filtered_sentences[idx])

    def edit_sentence_dialog(self, sentence):
        dialog = tk.Toplevel(self)
        dialog.title("Редактирование")
        dialog.geometry("600x400")
        tk.Label(dialog, text="Текст:").pack(pady=5)
        text_edit = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, height=5)
        text_edit.insert(tk.END, sentence.text)
        text_edit.pack(fill=tk.X, padx=10, pady=5)
        def save_changes():
            new_text = text_edit.get("1.0", tk.END).strip()
            if not new_text:
                messagebox.showerror("Ошибка", "Введите текст")
                return
            for i, sent in enumerate(self.sentences):
                if sent.text == sentence.text:
                    doc = nlp(new_text)
                    if len(list(doc.sents)) != 1:
                        messagebox.showerror("Ошибка", "Введите одно предложение")
                        return
                    new_sent = list(doc.sents)[0]
                    tokens_info = []
                    semantic_info = []
                    subjects = []
                    predicates = []
                    objects = []
                    attributes = []
                    adverbials = []
                    for token in new_sent:
                        tokens_info.append(f"{token.text} ({token.pos_}) -> {token.dep_} -> {token.head.text}")
                        semantic_info.append(self.get_semantic_info(token.text))
                        if token.dep_ in ["nsubj", "nsubj:pass"]:
                            subjects.append(token.text)
                        elif token.pos_ == "VERB" or token.dep_ == "ROOT":
                            predicates.append(token.text)
                        elif token.dep_ in ["obj", "iobj", "obl"]:
                            objects.append(token.text)
                        elif token.dep_ in ["amod", "nummod"]:
                            attributes.append(token.text)
                        elif token.dep_ in ["advmod", "nmod"]:
                            adverbials.append(token.text)
                    self.sentences[i] = SentenceData(
                        text=new_text,
                        tokens=tokens_info,
                        semantic_analysis=semantic_info,
                        tree_root=self.build_syntax_tree(new_sent),
                        subjects=subjects,
                        predicates=predicates,
                        objects=objects,
                        attributes=attributes,
                        adverbials=adverbials
                    )
                    break
            self.filtered_sentences = self.sentences.copy()
            self.refresh_treeview()
            dialog.destroy()
        tk.Button(dialog, text="Сохранить", command=save_changes).pack(pady=10)

    def show_help(self):
        help_window = tk.Toplevel(self)
        help_window.title("Справка")
        help_window.geometry("700x500")
        text = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True)
        help_content = """Синтаксический анализатор:
1. Открывайте PDF-файлы
2. Анализируйте предложения
3. Редактируйте текст
4. Сохраняйте результаты"""
        text.insert(tk.END, help_content)
        text.config(state=tk.DISABLED)
        tk.Button(help_window, text="Закрыть", command=help_window.destroy).pack(pady=10)

def main():
    app = SyntaxApp()
    app.mainloop()

if __name__ == "__main__":
    main()
