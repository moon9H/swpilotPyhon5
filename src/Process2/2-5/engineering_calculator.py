import sys
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLineEdit,
)
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 수직 레이아웃 및 디스플레이 창 추가
        layout = QVBoxLayout()
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet(
            """
            font-size: 28px;
            height: 60px;
            padding-right: 10px;
            background-color : black
            """
            )
        layout.addWidget(self.display)
        

        # 그리드 레이아웃 생성
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)  # 버튼 간의 여백을 최소화

        # 버튼의 텍스트 및 그리드 위치 설정
        button_positions = {
            (0, 0): '(',   (0, 1): ')',   (0, 2): 'mc',  (0, 3): 'm+',  (0, 4): 'm-',  (0, 5): 'mr',   (0, 6): "AC", (0, 7): "+/-", (0, 8): "%", (0, 9): "÷",
            (1, 0): '2nd', (1, 1): 'x^2', (1, 2): 'x^3', (1, 3): 'x^y', (1, 4): 'e^x', (1, 5): '10^x', (1, 6): "7",  (1, 7): "8",   (1, 8): "9", (1, 9): "x",
            (2, 0): '1/x', (2, 1): '2√x', (2, 2): '3√x', (2, 3): 'y√x', (2, 4): 'ln',  (2, 5): 'log10',(2, 6): "4",  (2, 7): "5",   (2, 8): "6", (2, 9): "-",
            (3, 0): 'x!', (3, 1): 'sin', (3, 2): 'cos', (3, 3): 'tan',  (3, 4): 'e',   (3, 5): 'EE',   (3, 6): "1",  (3, 7): "2",   (3, 8): "3", (3, 9): "+",
            (4, 0): 'Rad', (4, 1): 'sinh', (4, 2): 'cosh', (4, 3): 'tanh',  (4, 4): 'π',   (4, 5): 'Rand', (4, 6): "0",  (4, 7): "",  (4, 8): ".", (4, 9): "=",
        }

        # 그리드 레이아웃에 버튼 추가
        for position, text in button_positions.items():
            if position == (4, 6) or position == (4, 7):
                # 0 버튼이 두 열을 차지하도록
                button = QPushButton("0")
                button.setStyleSheet("background-color : rgb(red,green,blue); color : white")
                button.setMinimumSize(100, 50)  # 두 칸을 차지하도록 설정
                button.clicked.connect(self.button_clicked)
                grid_layout.addWidget(button, 4, 6, 1, 2)  # 1행 2열 크기
            elif text:
                button = QPushButton(text)
                button.setStyleSheet("background-color : rgb(red,green,blue); color : white")
                button.setMinimumSize(50, 50)  # 두 칸을 차지하도록 설정
                button.clicked.connect(self.button_clicked)
                grid_layout.addWidget(button, *position)
            else:
                # 빈칸을 만들기 위해 빈 위젯 추가
                empty_widget = QWidget()
                grid_layout.addWidget(empty_widget, *position)
        # 그리드 레이아웃을 수직 레이아웃에 추가
        layout.addLayout(grid_layout)

        # 전체 레이아웃 설정
        self.setLayout(layout)
        self.setWindowTitle("Engineering Calculator")
        self.setGeometry(100, 100, 500, 300)
        self.setStyleSheet("background-color: black")


    def button_clicked(self):
        # 버튼 클릭 이벤트 처리
        button = self.sender()  # 클릭된 버튼을 가져옴
        text = button.text()
        
        if text.isdigit():  # 숫자 버튼이 눌린 경우
            # 현재 디스플레이 텍스트를 가져옴
            current_text = self.display.text().replace(',', '')  # 콤마 제거
            new_text = current_text + text  # 새 텍스트 추가

            # 숫자로 변환하여 세자리마다 콤마를 추가
            formatted_text = "{:,}".format(int(new_text))
            
            # 디스플레이에 설정
            self.display.setText(formatted_text)
        else:
            # 다른 비-숫자 버튼을 눌렀을 때 처리
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())