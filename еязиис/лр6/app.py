# flask run --host=0.0.0.0 --port=5000
# what is the most popular animal?

from flask import Flask, request, render_template, jsonify
import os
import json
from g4f.client import Client
import g4f

from dialog_system import get_answer_tfidf, save_qa_to_file
from question_filter import is_animals_question

app = Flask(__name__)
CHAT_FILE = 'chats.json'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/create_chat', methods=['POST'])
def create_chat():
    data = request.get_json()
    chat_name = data.get('chat_name')
    if not chat_name:
        return jsonify(success=False), 400

    if not os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, 'w') as f:
            json.dump([], f)

    chat_filename = f'chat_{chat_name}.json'
    if not os.path.exists(chat_filename):
        with open(chat_filename, 'w') as f:
            json.dump([], f)

    with open(CHAT_FILE, 'r+') as f:
        try:
            chats = json.load(f)
            if not isinstance(chats, list):  # Защита от неверного формата
                chats = []
        except json.JSONDecodeError:
            chats = []

        if chat_name not in chats:
            chats.append(chat_name)
            f.seek(0)
            json.dump(chats, f, indent=2)
            f.truncate()

    return jsonify(success=True)

@app.route('/get_chats')
def get_chats():
    if not os.path.exists(CHAT_FILE):
        return jsonify([])
    with open(CHAT_FILE, 'r') as f:
        return jsonify(json.load(f))

@app.route('/get_history/<chat_name>')
def get_history(chat_name):
    chat_filename = f'chat_{chat_name}.json'
    if not os.path.exists(chat_filename):
        return jsonify([])
    with open(chat_filename, 'r', encoding='utf-8') as f:
        try:
            return jsonify(json.load(f))
        except json.JSONDecodeError:
            return jsonify([])


@app.route('/chat/<chat_name>')
def chat_window(chat_name):
    return render_template('chat.html', chat_name=chat_name)

@app.route('/send_message', methods=['POST'])
def send_message():
    client = Client()
    data = request.get_json()
    user_message = data.get('message')
    chat_name = data.get('chat_name')

    if not user_message or not chat_name:
        return jsonify({'error': 'Missing message or chat name'}), 400

    try:
        if is_animals_question(user_message):
            answer = get_answer_tfidf(user_question=user_message)
            if answer is None:
                # Получаем ответ от GPT
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": user_message}],
                )
                answer = response.choices[0].message.content
                save_qa_to_file(user_message, answer)
        else:
            answer = "Question not related to animals. Try again"

        # Сохраняем в файл
        chat_filename = f'chat_{chat_name}.json'
        if not os.path.exists(chat_filename):
            with open(chat_filename, 'w') as f:
                json.dump([], f)

        with open(chat_filename, 'r+', encoding='utf-8') as f:
            try:
                history = json.load(f)
                if not isinstance(history, list):
                    history = []
            except json.JSONDecodeError:
                history = []

            history.append({"sender": "user", "message": user_message})
            history.append({"sender": "gpt", "message": answer})

            f.seek(0)
            json.dump(history, f, indent=2, ensure_ascii=False)
            f.truncate()

        return jsonify({'response': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/delete_chat/<chat_name>", methods=["DELETE"])
def delete_chat(chat_name):
    # Формирование пути к файлу чата в корне проекта
    filename = f"chat_{chat_name}.json"

    if os.path.exists(filename):
        os.remove(filename)  # Удаление файла чата
        delete_chat_from_list(chat_name)  # Удаление чата из списка в chats.json
        return "", 204  # Статус 204 (No Content)
    else:
        return jsonify({"error": "Chat not found"}), 404  # Статус 404 (Not Found)


def delete_chat_from_list(chat_name):
    CHATS_FILE = 'chats.json'  
    with open(CHATS_FILE, 'r', encoding='utf-8') as f:
        chats = json.load(f)

    if chat_name in chats:
        chats.remove(chat_name)

    # Перезапись обновленного списка в файл
    with open(CHATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(chats, f, ensure_ascii=False, indent=4)