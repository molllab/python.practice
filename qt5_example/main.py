# PyQt 기본 틀
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DemoWindow 타이틀")
        self.setGeometry(300, 300, 300, 400)

        btn1 = QPushButton("클릭하기", self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn1_clicked)

    def btn1_clicked(self):
        QMessageBox.about(self, "title", "contents")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = DemoWindow()
    demoWindow.show()
    app.exec_()