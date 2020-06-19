import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel
from preprocessing import QueryProcessor
from PyQt5.QtCore import pyqtSlot


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'පද රචනා සෙවුම් යන්ත්‍රය'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 640
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox
        self.search_box = QLineEdit(self)
        self.search_box.move(20, 20)
        self.search_box.resize(280, 40)

        # Create a button in the window
        self.search_button = QPushButton('සෙවීම', self)
        self.search_button.move(320, 20)

        # connect button to function on_click
        self.search_button.clicked.connect(self.search_query)

        self.artist_label = QLabel(self)
        self.artist_label.setText("කලාකරු")
        self.artist_label.move(20, 90)
        self.artist_search_box = QLineEdit(self)
        self.artist_search_box.move(100, 90)
        self.artist_search_box.resize(280, 30)

        self.composer_label = QLabel(self)
        self.composer_label.setText("නිර්මාපකය")
        self.composer_label.move(20, 160)
        self.composer_search_box = QLineEdit(self)
        self.composer_search_box.move(100, 160)
        self.composer_search_box.resize(280, 30)

        self.writer_label = QLabel(self)
        self.writer_label.setText("ලේඛකයා")
        self.writer_label.move(20, 230)
        self.writer_search_box = QLineEdit(self)
        self.writer_search_box.move(100, 230)
        self.writer_search_box.resize(280, 30)

        self.key_label = QLabel(self)
        self.key_label.setText("Key")
        self.key_label.move(20, 300)
        self.key_search_box = QLineEdit(self)
        self.key_search_box.move(100, 300)
        self.key_search_box.resize(280, 30)

        self.beat_label = QLabel(self)
        self.beat_label.setText("Beat")
        self.beat_label.move(20, 370)
        self.beat_search_box = QLineEdit(self)
        self.beat_search_box.move(100, 370)
        self.beat_search_box.resize(280, 30)

        self.movie_label = QLabel(self)
        self.movie_label.setText("චිත්රපටය")
        self.movie_label.move(20, 440)
        self.movie_search_box = QLineEdit(self)
        self.movie_search_box.move(100, 440)
        self.movie_search_box.resize(280, 30)

        self.title_label = QLabel(self)
        self.title_label.setText("නම")
        self.title_label.move(20, 510)
        self.title_search_box = QLineEdit(self)
        self.title_search_box.move(100, 510)
        self.title_search_box.resize(280, 30)

        self.lyrics_label = QLabel(self)
        self.lyrics_label.setText("සින්‌දු")
        self.lyrics_label.move(20, 580)
        self.lyrics_search_box = QLineEdit(self)
        self.lyrics_search_box.move(100, 580)
        self.lyrics_search_box.resize(280, 30)

        self.show()

    @pyqtSlot()
    def search_query(self):
        facetedQuery = {
            "artist": self.artist_search_box.text(),
            "composer": self.composer_search_box.text(),
            "writer": self.writer_search_box.text(),
            "key": self.key_search_box.text(),
            "beat": self.beat_search_box.text(),
            "movie": self.movie_search_box.text(),
            "lyrics": self.lyrics_search_box.text(),
            "title": self.title_search_box.text()
        }
        isFaceted = False
        for i in facetedQuery:
            if facetedQuery[i] != None and facetedQuery[i] != "":
                isFaceted = True
                break
        if (not isFaceted):
            searchQuery = self.search_box.text()
            print(searchQuery)
            qp.generateQuery(searchQuery)
        else:
            qp.advancedQuery(facetedQuery)

        self.artist_search_box.setText("")
        self.composer_search_box.setText("")
        self.writer_search_box.setText("")
        self.key_search_box.setText("")
        self.beat_search_box.setText("")
        self.movie_search_box.setText("")
        self.lyrics_search_box.setText("")
        self.title_search_box.setText("")
        self.search_box.setText("")


if __name__ == '__main__':
    qp = QueryProcessor()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
