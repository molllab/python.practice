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
        self.cnt_bracket = 0
        self.dot_ok = True

        self.btn_map = [
            ['+', '-', '*', '/'],
            ['1', '2', '3', 'del'],
            ['4', '5', '6', 'clear'],
            ['7', '8', '9', '.'],
            ['(', ')', '0', '=']
        ]

        btn_obj = []

        for i, row in enumerate(self.btn_map):
            for j, ch in enumerate(row):
                btn_obj.append(QPushButton(ch, self))
                tmp = btn_obj[-1]
                tmp.move(tmp.width()*j, tmp.height()*i + label_height)
                tmp.clicked.connect(self.on_btn_clicked)

    def error_check(self, formula):
        if self.disp_str[-2:] == '/0':
            QMessageBox.about(self, "수식오류", "0으로 나눌 수 없습니다.")
            return False

        try:
            eval(formula)
        except:
            QMessageBox.about(self, "수식오류", "수식을 정확히 입력해주세요.")
            return False

        if self.cnt_bracket != 0:
            QMessageBox.about(self, "수식오류", "괄호의 개수를 정확히 입력하세요")
            return False
        
        return True

    def on_btn_clicked(self):
        btn_name = self.sender().text()
        
        if btn_name in ['+', '-', '*', '/']:
            if len(self.disp_str):
                if self.disp_str[-1] not in ['+', '-', '*', '/']:
                    if self.disp_str[-1] == '.':
                        self.disp_str = self.disp_str[:-1]
                    
                    self.disp_str += btn_name
                    self.dot_ok = True

        elif btn_name == 'del':
            self.disp_str = self.disp_str[:-1]
        
        elif btn_name == 'clear':
            self.disp_str = ""

        elif btn_name == '.':
            if self.dot_ok:
                self.disp_str += btn_name
                self.dot_ok = False
        
        elif btn_name == '=':
            if self.disp_str[-1] in ['+', '-', '*', '/']:
                pass

            else:
                if self.error_check(self.disp_str):
                    res = eval(self.disp_str)
                    if isinstance(res, int):
                        self.disp_str = str(res)
                    elif isinstance(res, float):
                        self.disp_str = str(round(res, 4))
                
                else:
                    self.disp_str = ""
                    self.res_label.setText(self.disp_str)

        elif btn_name in [ '0', '00' ]:
            if self.disp_str == "" and btn_name == '00':
                btn_name = '0'
            
            self.disp_str += btn_name

        else:
            if btn_name == '(':
                self.cnt_bracket += 1
            elif btn_name == ')':
                self.cnt_bracket -= 1

            self.disp_str += btn_name
            
        self.res_label.setText(self.disp_str)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = DemoWindow()
    demoWindow.show()
    app.exec_()