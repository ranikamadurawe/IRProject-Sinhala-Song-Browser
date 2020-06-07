import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel
import preprocessing
from PyQt5.QtCore import pyqtSlot




class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'පද රචනා සෙවුම් යන්ත්‍රය'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 600
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textbox
        self.search_box = QLineEdit(self)
        self.search_box.move(20, 20)
        self.search_box.resize(280,40)
        
        # Create a button in the window
        self.search_button = QPushButton('සෙවීම', self)
        self.search_button.move(320,20)
        
        # connect button to function on_click
        self.search_button.clicked.connect(self.search_query)
	
        self.artist_label = QLabel(self)
        self.artist_label.setText("කලාකරු")
        self.artist_label.move(20, 90)
        self.artist_search_box = QLineEdit(self)
        self.artist_search_box.move(100, 90)
        self.artist_search_box.resize(280,30)

        self.composer_label = QLabel(self)
        self.composer_label.setText("නිර්මාපකය")
        self.composer_label.move(20, 160)
        self.composer_search_box = QLineEdit(self)
        self.composer_search_box.move(100, 160)
        self.composer_search_box.resize(280,30)

        self.writer_label = QLabel(self)
        self.writer_label.setText("ලේඛකයා")
        self.writer_label.move(20, 230)
        self.writer_search_box = QLineEdit(self)
        self.writer_search_box.move(100, 230)
        self.writer_search_box.resize(280,30)

        self.key_label = QLabel(self)
        self.key_label.setText("Key")
        self.key_label.move(20, 300)
        self.key_search_box = QLineEdit(self)
        self.key_search_box.move(100, 300)
        self.key_search_box.resize(280,30)

        self.beat_label = QLabel(self)
        self.beat_label.setText("Beat")
        self.beat_label.move(20, 370)
        self.beat_search_box = QLineEdit(self)
        self.beat_search_box.move(100, 370)
        self.beat_search_box.resize(280,30)

        self.movie_label = QLabel(self)
        self.movie_label.setText("චිත්රපටය")
        self.movie_label.move(20, 440)
        self.movie_search_box = QLineEdit(self)
        self.movie_search_box.move(100, 440)
        self.movie_search_box.resize(280,30)

        self.show()
    
    @pyqtSlot()
    def search_query(self):
        searchQuery = self.search_box.text()
        preprocessing.generateNormalQuery(searchQuery)
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + ",".join(searchQuery), QMessageBox.Ok, QMessageBox.Ok)
        self.search_box.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


