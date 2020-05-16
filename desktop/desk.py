import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from client2 import get_articles
from pymongo import MongoClient

SERVER_HOST = 'mongodb://localhost:27017/'
SERVER_DB = 'verge'
SERVER_COLLECTION = 'articles_stats'

LIKE = 'like'
DISLIKE = 'dislike'

id_list, title_list, author_list, href_list = get_articles()

app = QApplication(sys.argv)
widget = QWidget()
layout = QGridLayout()
widget.setLayout(layout)

radio_buttons = {}


def window():
    for i in range(len(id_list)):
        radiobutton1 = QRadioButton("Like")
        radiobutton2 = QRadioButton("Dislike")
        radio_buttons[title_list[i]] = {'like': radiobutton1, 'dislike': radiobutton2}
        group_box = QGroupBox(f"{title_list[i]}")
        box_layout = QVBoxLayout()

        box_layout.addWidget(radiobutton1)

        box_layout.addWidget(radiobutton2)

        group_box.setLayout(box_layout)
        layout.addWidget(group_box, 0 + i*10, 0)

    button1 = QPushButton(widget)
    button1.setText("Submit")
    button1.move(15, 735)
    button1.clicked.connect(clicked)

    widget.setGeometry(50, 50, 840, 600)
    widget.setWindowTitle("Example")
    widget.show()
    sys.exit(app.exec_())


def clicked():
    for title in radio_buttons:
        if radio_buttons[title]['like'].isChecked() is False and radio_buttons[title]['dislike'].isChecked() is False:
            continue
        elif radio_buttons[title]['like'].isChecked():
            print(title)
            print('like')
            store_in_db(title, ld_value='like')
        else:
            print(title)
            print('dislike')
            store_in_db(title, ld_value='dislike')


def store_in_db(article_id, ld_value):
    client = MongoClient(SERVER_HOST)
    db = client[SERVER_DB]
    col = db[SERVER_COLLECTION]
    col.insert_one({
        "article_id": article_id,
        "like_dislike": ld_value,
        "app_type": "desk"
    })


if __name__ == '__main__':
    window()
