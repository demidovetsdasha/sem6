import spacy
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
from dataclasses import dataclass, field
import csv
import time
from pdfminer.high_level import extract_text
from typing import List, Optional
import sys
import tempfile
import os
import xml.etree.ElementTree as ET
from anytree import Node, RenderTree
import matplotlib.pyplot as plt
from anytree.exporter.dotexporter import DotExporter

try:
    nlp = spacy.load("ru_core_news_sm")
except OSError:
    messagebox.showerror("Ошибка", "Установите модель: python -m spacy download ru_core_news_sm")
    exit()

pp_index = 0
np_index = 0
vp_index = 0
word_index = 0

sys.setrecursionlimit(10000)

@dataclass
class TreeNode:
    label: str
    text: str = ""
    children: List['TreeNode'] = field(default_factory=list)
    parent: Optional['TreeNode'] = None

@dataclass
class SentenceData:
    text: str
    tokens: list
    tree_root: Optional[TreeNode] = None
    subjects: list = field(default_factory=list)
    predicates: list = field(default_factory=list)
    objects: list = field(default_factory=list)
    attributes: list = field(default_factory=list)
    adverbials: list = field(default_factory=list)

class SyntaxApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Синтаксический анализ")
        self.geometry("1200x800")
        self.sentences = []
        self.filtered_sentences = []
        self.current_file = ""
        self.create_menu()
        self.create_widgets()
        self.create_help_tab()
        self.token_to_phrase = {}

    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Открыть PDF", command=self.load_file)
        file_menu.add_command(label="Сохранить XML", command=self.save_result_xml)
        file_menu.add_command(label="Сохранить TXT", command=self.save_result_txt)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        analysis_menu = tk.Menu(menubar, tearoff=0)
        analysis_menu.add_command(label="Статистика", command=self.show_members_stats)
        analysis_menu.add_command(label="Поиск по членам", command=self.find_by_members_dialog)
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

        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        columns = ("text", "subjects", "predicates", "objects", "attributes", "adverbials")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                 yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, height=15)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100 if col != "text" else 300)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        self.notebook = ttk.Notebook(display_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        members_frame = tk.Frame(self.notebook)
        self.members_text = scrolledtext.ScrolledText(members_frame, wrap=tk.WORD, height=10)
        self.members_text.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(members_frame, text="Разбор")

        tokens_frame = tk.Frame(self.notebook)
        self.tokens_text = scrolledtext.ScrolledText(tokens_frame, wrap=tk.WORD, height=10)
        self.tokens_text.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(tokens_frame, text="Токены")

        self.status_bar = tk.Label(self, text="Готово", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X)

        self.tree.bind("<<TreeviewSelect>>", self.show_sentence_details)
        self.tree.bind("<Double-1>", self.edit_sentence)

    def create_help_tab(self):
        help_frame = tk.Frame(self.notebook)
        help_text = scrolledtext.ScrolledText(help_frame, wrap=tk.WORD, height=10)
        help_text.pack(fill=tk.BOTH, expand=True)
        help_content = """Синтаксический анализатор:
1. Откройте PDF-файл через меню Файл
2. Выберите предложение в таблице
3. Анализируйте дерево зависимостей
4. Используйте фильтр для поиска
5. Сохраняйте результаты в XML/TXT"""
        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)
        self.notebook.add(help_frame, text="Справка")

    def build_syntax_tree(self, sent):
        root = TreeNode(label="S")
        pos_indices = {}
        nodes = {}
        self.token_to_phrase.clear()
        processed = set()
        indices = {'np': 0, 'vp': 0, 'pp': 0}

        # Создание узлов
        for token in sent:
            pos = token.pos_.upper()
            pos_indices[pos] = pos_indices.get(pos, -1) + 1
            label = f"{pos}{pos_indices[pos]}"
            nodes[token] = TreeNode(label=label, text=token.text)

        # Подлежащие
        subjects = []
        for token in sent:
            if token.dep_ in ["nsubj", "nsubj:pass"]:
                subjects.append(token)
                for child in token.children:
                    if child.dep_ == "conj" and child.pos_ in ["NOUN", "PROPN", "PRON"]:
                        subjects.append(child)
        subjects = list(dict.fromkeys(subjects))
        for subj in subjects:
            if subj not in processed:
                indices['np'] += 1
                np = TreeNode(label=f"NP{indices['np']}")
                self.build_np(np, subj, nodes, processed, indices)
                root.children.append(np)
                np.parent = root

        # Сказуемые
        verbs = []
        for token in sent:
            if token.pos_ == "VERB" or token.dep_ == "ROOT":
                verbs.append(token)
                for child in token.children:
                    if child.dep_ == "conj" and child.pos_ == "VERB":
                        verbs.append(child)
        verbs = list(dict.fromkeys(verbs))
        for verb in verbs:
            if verb not in processed:
                indices['vp'] += 1
                vp = TreeNode(label=f"VP{indices['vp']}")
                self.build_vp(vp, verb, nodes, processed, indices)
                root.children.append(vp)
                vp.parent = root

        # Предлоги
        for token in sent:
            if token.dep_ == "case" and token.pos_ == "ADP" and token not in processed:
                self.process_preposition(token, root, nodes, processed, indices)

        return root

    def build_np(self, np_node, head, nodes, processed, indices):
        if head in processed:
            return
        processed.add(head)
        self.token_to_phrase[head] = np_node
        np_node.children.append(nodes[head])
        nodes[head].parent = np_node

        for child in head.children:
            if child.dep_ in {"det", "amod", "nummod", "acl", "nmod"}:
                self.build_np(np_node, child, nodes, processed, indices)

    def build_vp(self, vp_node, head, nodes, processed, indices):
        if head in processed:
            return
        processed.add(head)
        self.token_to_phrase[head] = vp_node
        vp_node.children.append(nodes[head])
        nodes[head].parent = vp_node

        for child in head.children:
            if child.dep_ in {"obj", "iobj", "obl", "advmod", "xcomp"}:
                self.build_vp_child(vp_node, child, nodes, processed, indices)

    def build_vp_child(self, parent_node, child, nodes, processed, indices):
        if child in processed:
            return
        processed.add(child)
        self.token_to_phrase[child] = parent_node
        parent_node.children.append(nodes[child])
        nodes[child].parent = parent_node

        for grandchild in child.children:
            if grandchild.dep_ in {"obj", "obl", "advmod"}:
                self.build_vp_child(parent_node, grandchild, nodes, processed, indices)

    def process_preposition(self, prep, root, nodes, processed, indices):
        objs = [ch for ch in prep.children
                if ch.dep_ in {"obj", "obl", "nmod"} and ch.pos_ in {"NOUN", "PROPN", "PRON"}]
        if not objs:
            return

        indices['pp'] += 1
        pp = TreeNode(label=f"PP{indices['pp']}")
        processed.add(prep)
        pp.children.append(nodes[prep])
        nodes[prep].parent = pp

        for obj in objs:
            if obj in processed:
                continue
            indices['np'] += 1
            inner_np = TreeNode(label=f"NP{indices['np']}")
            self.build_np(inner_np, obj, nodes, processed, indices)
            pp.children.append(inner_np)
            inner_np.parent = pp

        gov = prep.head
        phrase_node = self.token_to_phrase.get(gov)
        if phrase_node:
            phrase_node.children.append(pp)
            pp.parent = phrase_node
        else:
            root.children.append(pp)
            pp.parent = root


    def convert_to_anytree(self, node, parent=None):
        name = f"{node.label}\n{node.text}" if node.text else node.label
        any_node = Node(name, parent=parent)
        for child in node.children:
            self.convert_to_anytree(child, any_node)
        return any_node

    def visualize_tree(self, root_node):
        try:
            temp_dir = os.getenv('TEMP')
            dot_path = os.path.join(temp_dir, f"tree_{os.getpid()}.dot")
            png_path = os.path.join(temp_dir, f"tree_{os.getpid()}.png")

            anytree_root = self.convert_to_anytree(root_node)
            DotExporter(anytree_root,
                        nodeattrfunc=lambda node: f'label="{node.name}" shape=box',
                        edgeattrfunc=lambda parent, child: 'arrowsize=0.5'
                        ).to_dotfile(dot_path)

            os.system(f'dot -Tpng "{dot_path}" -o "{png_path}"')
            if sys.platform == "win32":
                os.startfile(png_path)
            else:
                os.system(f'xdg-open "{png_path}"')

            time.sleep(1)
            if os.path.exists(dot_path):
                os.remove(dot_path)
            if os.path.exists(png_path):
                os.remove(png_path)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка генерации дерева: {str(e)}")

    def show_sentence_details(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        idx = self.tree.index(selected_item)
        if 0 <= idx < len(self.filtered_sentences):
            sent = self.filtered_sentences[idx]

            self.members_text.config(state=tk.NORMAL)
            self.members_text.delete(1.0, tk.END)
            self.members_text.insert(tk.END, f"Предложение: {sent.text}\n\n")
            self.members_text.insert(tk.END, "Подлежащие:\n" + "\n".join(f"- {s}" for s in sent.subjects) + "\n\n")
            self.members_text.insert(tk.END, "Сказуемые:\n" + "\n".join(f"- {p}" for p in sent.predicates) + "\n\n")
            self.members_text.insert(tk.END, "Дополнения:\n" + "\n".join(f"- {o}" for o in sent.objects) + "\n\n")
            self.members_text.insert(tk.END, "Определения:\n" + "\n".join(f"- {a}" for a in sent.attributes) + "\n\n")
            self.members_text.insert(tk.END, "Обстоятельства:\n" + "\n".join(f"- {a}" for a in sent.adverbials) + "\n")
            self.members_text.config(state=tk.DISABLED)

            self.tokens_text.config(state=tk.NORMAL)
            self.tokens_text.delete(1.0, tk.END)
            self.tokens_text.insert(tk.END, "Токены:\n\n" + "\n".join(f"- {t}" for t in sent.tokens))
            self.tokens_text.config(state=tk.DISABLED)

            self.visualize_tree(sent.tree_root)

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Выберите PDF", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

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
                subjects = []
                predicates = []
                objects = []
                attributes = []
                adverbials = []

                for token in sent:
                    tokens_info.append(f"{token.text} ({token.pos_}) -> {token.dep_} -> {token.head.text}")


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
            short_text = (sent.text[:100] + '...') if len(sent.text) > 100 else sent.text
            self.tree.insert("", tk.END, values=(
                short_text,
                ", ".join(sent.subjects) if sent.subjects else "-",
                ", ".join(sent.predicates) if sent.predicates else "-",
                ", ".join(sent.objects) if sent.objects else "-",
                ", ".join(sent.attributes) if sent.attributes else "-",
                ", ".join(sent.adverbials) if sent.adverbials else "-"
            ))

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
            text.insert(tk.END, f"{k}: {v} (среднее: {v / total:.1f})\n")
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


    def save_result_xml(self):
        if not self.sentences:
            messagebox.showwarning("Ошибка", "Нет данных для сохранения")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if not file_path:
            return

        try:
            root = ET.Element("root")

            # Имя исходного файла (если было загружено)
            if hasattr(self, "loaded_file_path") and self.loaded_file_path:
                root.set("file", os.path.basename(self.loaded_file_path))
            else:
                root.set("file", "output.pdf")

            for idx, sent in enumerate(self.sentences, start=1):
                sentence_elem = ET.SubElement(root, "sentence", id=str(idx))

                full_sentence = ET.SubElement(sentence_elem, "full_sentence")
                full_sentence.text = sent.text.strip()

                # Объединяем все слова, чтобы сохранить их в виде word-тегов
                all_words = (
                    [(w, "Подлежащие") for w in sent.subjects] +
                    [(w, "Сказуемые") for w in sent.predicates] +
                    [(w, "Дополнения") for w in sent.objects] +
                    [(w, "Определения") for w in sent.attributes] +
                    [(w, "Обстоятельства") for w in sent.adverbials]
                )

                used = set()
                word_id = 1
                for word, morph_info in all_words:
                    if word not in used:  # Избегаем дублирования слов
                        word_elem = ET.SubElement(sentence_elem, "word", id=str(word_id), info=f"Часть речи: {morph_info}")
                        word_elem.text = word
                        used.add(word)
                        word_id += 1

            # Сохраняем XML в выбранный файл
            tree = ET.ElementTree(root)
            tree.write(file_path, encoding="utf-8", xml_declaration=True)

            messagebox.showinfo("Успех", f"Результаты сохранены в {file_path}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")
        

    def save_result_csv(self):
        if not self.sentences:
            messagebox.showwarning("Ошибка", "Нет данных")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
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
        if not file_path:
            return
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
                    f.write("\n" + "=" * 80 + "\n\n")
                messagebox.showinfo("Успех", f"Сохранено в {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")

    def auto_filter(self):
        filter_text = self.sentence_filter_entry.get().lower()
        self.filtered_sentences = [sent for sent in self.sentences if filter_text in sent.text.lower()]
        self.refresh_treeview()

    def edit_sentence(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
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
                    subjects = []
                    predicates = []
                    objects = []
                    attributes = []
                    adverbials = []
                    for token in new_sent:
                        tokens_info.append(f"{token.text} ({token.pos_}) -> {token.dep_} -> {token.head.text}")
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
