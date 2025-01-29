from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLineEdit, \
    QListWidget, QMessageBox
import os
import json

FILENAME = 'notes.json'
notes = {
    'Приветствие' : {
        'text' : 'Добро пожаловать',
        'tags' : ['Привет']
    },
    'Инструкция' : {
        'text' : 'Нажмите кнопку сохранить заметку, чтобы сохранить заметку',
        'tags' : []
    }
}

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('SmartNotes')
main_win.setFixedSize(800, 600)

layout_main = QHBoxLayout()
layout_v = QVBoxLayout()
layout_h_sup1 = QHBoxLayout()
layout_h_sup2 = QHBoxLayout()
layout_h_sup3 = QHBoxLayout()
layout_h_sup4 = QHBoxLayout()
note_text = QTextEdit()
note_text.setPlaceholderText('Напишите заметку')
label_list_notes = QLabel('Список заметок')
list_notes = QListWidget()
note_name_edit = QLineEdit()
note_name_edit.setPlaceholderText('Введите название заметки...')
create_button = QPushButton('Создать заметку')
delete_button = QPushButton('Удалить заметку')
save_button = QPushButton('Сохранить заметку')
label_list_teg = QLabel('Список тегов')
tag_list = QListWidget()
tag_name_edit = QLineEdit()
tag_name_edit.setPlaceholderText('Введите тег...')
add_tag_button = QPushButton('Добавить к заметке')
unpin_tag_button = QPushButton('Открепить от заметки')
reset_button = QPushButton('Сбросить поиск')
search_button = QPushButton('Искать заметки по тегу')

layout_v.addWidget(label_list_notes, alignment=Qt.AlignmentFlag.AlignLeft)
layout_v.addWidget(list_notes)
layout_h_sup1.addWidget(save_button)
layout_h_sup1.addWidget(delete_button)
layout_h_sup2.addWidget(note_name_edit)
layout_h_sup2.addWidget(create_button)
layout_v.addLayout(layout_h_sup1)
layout_v.addLayout(layout_h_sup2)
layout_v.addWidget(label_list_teg, alignment=Qt.AlignmentFlag.AlignLeft)
layout_v.addWidget(tag_list)
layout_v.addWidget(tag_name_edit)
layout_h_sup3.addWidget(add_tag_button)
layout_h_sup3.addWidget(unpin_tag_button)
layout_h_sup4.addWidget(search_button)
layout_h_sup4.addWidget(reset_button)
layout_v.addLayout(layout_h_sup3)
layout_v.addLayout(layout_h_sup4)
layout_main.addWidget(note_text)
layout_main.addLayout(layout_v)
main_win.setLayout(layout_main)

def save_data():
    with open(FILENAME, "w") as file:
        json.dump(notes, file, indent=4)

if os.path.exists(FILENAME) and os.path.isfile(FILENAME):
    with open(FILENAME, 'r') as file:
        notes = json.load(file)
else:
    save_data()
list_notes.addItems(notes)



def show_note():
    name = list_notes.selectedItems()[0].text()
    text = notes[name]['text']
    tags = notes[name]['tags']
    note_text.setText(text)
    tag_list.clear()
    tag_list.addItems(tags)

def save_note():
    if len(list_notes.selectedItems()) == 0:
        msg = QMessageBox()
        msg.setWindowTitle('Ошибка')
        msg.setText('Выделите заметку для сохранения текста')
        msg.exec()
        return
    name = list_notes.selectedItems()[0].text()
    text = note_text.toPlainText()
    notes[name]['text'] = text
    save_data()

def delete_note():
    name = list_notes.selectedItems()[0].text()
    del notes[name]
    list_notes.clear()
    list_notes.addItems(notes)
    tag_list.clear()
    note_text.clear()
    save_data()

def create_note():
    name = note_name_edit.text()
    if len(name) == 0:
        msg = QMessageBox()
        msg.setWindowTitle('Ошибка')
        msg.setText('Введите название заметки для создания')
        msg.exec()
        return
    if name in notes.keys():
        msg = QMessageBox()
        msg.setWindowTitle('Ошибка')
        msg.setText('Такая заметка уже существует \n Введите другое название заметки ')
        msg.exec()
        return
    if name.isspace():
        msg = QMessageBox()
        msg.setWindowTitle('Ошибка')
        msg.setText('Название заметки должно состоять из строчных символов \n Введите другое название заметки ')
        msg.exec()
        return
    notes[name] = {'text':'','tags':[]}
    list_notes.clear()
    note_text.clear()
    tag_list.clear()
    list_notes.addItems(notes)
    save_data()

def add_tag():
    name_tag = tag_name_edit.text()
    name_note = list_notes.selectedItems()[0].text()
    if len(name_tag) == 0:
        msg = QMessageBox()
        msg.setWindowTitle('Ошибка')
        msg.setText('Введите название тега для создания')
        msg.exec()
        return
    if len(list_notes.selectedItems()) == 0:
        msg = QMessageBox()
        msg.setWindowTitle('Ошибка')
        msg.setText('Выделите заметку для добавления тега')
        msg.exec()
        return
    if name_tag in notes[name_note]['tags']:
        msg = QMessageBox()
        msg.setWindowTitle('Ошибка')
        msg.setText('Такой тег уже существует \n Введите другое название тега ')
        msg.exec()
        return
    if name_tag.isspace():
        msg = QMessageBox()
        msg.setWindowTitle('Ошибка')
        msg.setText('Название тега должно состоять из строчных символов \n Введите другое название тега ')
        msg.exec()
        return
    notes[name_note]['tags'].append(name_tag)
    tag_list.clear()
    tag_list.addItems(notes[name_note]['tags'])
    save_data()

def unpin_tag():
    if len(tag_list.selectedItems()) == 0:
        msg = QMessageBox()
        msg.setWindowTitle('Ошибка')
        msg.setText('Выделите тег для открепления от заметки')
        msg.exec()
        return
    if len(list_notes.selectedItems()) == 0:
        msg = QMessageBox()
        msg.setWindowTitle('Ошибка')
        msg.setText('Выделите заметку для открепления тега')
        msg.exec()
        return
    name_tag = tag_list.selectedItems()[0].text()
    name_note = list_notes.selectedItems()[0].text()
    notes[name_note]['tags'].remove(name_tag)
    tag_list.clear()
    tag_list.addItems(notes[name_note]['tags'])
    save_data()

def search_note():
    name_tag = tag_name_edit.text()
    if len(name_tag) == 0:
        msg = QMessageBox()
        msg.setWindowTitle('Ошибка')
        msg.setText('Введите название тега для поиска заметки')
        msg.exec()
        return
    search_note = []
    for name in notes:
        if name_tag in notes[name]['tags']:
            search_note.append(name)
    note_text.clear()
    list_notes.clear()
    list_notes.addItems(search_note)

def reset_search():
    list_notes.clear()
    list_notes.addItems(notes)
    tag_list.clear()
    note_text.clear()

reset_button.clicked.connect(reset_search)
search_button.clicked.connect(search_note)
unpin_tag_button.clicked.connect(unpin_tag)
add_tag_button.clicked.connect(add_tag)
create_button.clicked.connect(create_note)
delete_button.clicked.connect(delete_note)
save_button.clicked.connect(save_note)
list_notes.itemClicked.connect(show_note)
main_win.show()
app.exec()