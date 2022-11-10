# pip install pyqt5
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("나데연 계산기")
        self.setGeometry(300, 300, 400, 210)

        self.res_label = QLabel("", self)
        self.res_label.move(5,0)
        self.res_label.setFixedSize(400-10, 60)
        self.res_label.setAlignment(Qt.AlignRight)
        res_font = self.res_label.font()
        res_font.setPointSize(20)
        res_font.setBold(True)
        self.res_label.setFont(res_font)
        label_height = self.res_label.height()
        self.disp_str = ""

        self.btn_map = [
            ['+', '-', '*', '/'],
            ['1', '2', '3', 'del'],
            ['4', '5', '6', 'clear'],
            ['7', '8', '9', '='],
            ['00', '0', '.', None]
        ]

        btn_obj = []

        for i, row in enumerate(self.btn_map):
            for j, ch in enumerate(row):
                btn_obj.append(QPushButton(ch, self))
                tmp = btn_obj[-1]
                tmp.move(tmp.width()*j, tmp.height()*i + label_height)
                tmp.clicked.connect(self.on_btn_clicked)

    def on_btn_clicked(self):
        btn_name = self.sender().text()
        
        if btn_name in ['+', '-', '*', '/']:
            if len(self.disp_str):
                if self.disp_str[-1] not in ['+', '-', '*', '/']:
                    if self.disp_str[-1] == '.':
                        self.disp_str = self.disp_str[:-1]
                    
                    self.disp_str += btn_name

        elif btn_name == 'del':
            self.disp_str = self.disp_str[:-1]
        
        elif btn_name == 'clear':
            self.disp_str = ""
        
        elif btn_name == '=':
            if self.disp_str[-2:] == '/0':
                QMessageBox.about(self, "수식오류", "0으로 나눌 수 없습니다.")
            elif self.disp_str[-1] in ['+', '-', '*', '/']:
                pass
            else:
                res = eval(self.disp_str)
                if isinstance(res, int):
                    self.disp_str = str(int(res))
                elif isinstance(res, float):
                    self.disp_str = str(float(res))

        else:
            self.disp_str += btn_name

        self.res_label.setText(self.disp_str)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = DemoWindow()
    demoWindow.show()
    app.exec_()