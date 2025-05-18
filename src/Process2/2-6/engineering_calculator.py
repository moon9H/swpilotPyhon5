import sys
import math
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
        self.memory = 0  # 메모리 기능을 위한 변수
        self.pending_op = ""  # 대기 중인 연산자
        self.pending_value = ""  # 대기 중인 값
        self.second_mode = False  # 2nd 모드 활성화 상태

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
            """
        )
        layout.addWidget(self.display)

        # 그리드 레이아웃 생성
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)

        # 버튼의 텍스트 및 그리드 위치 설정
        button_positions = {
            (0, 0): '(',   (0, 1): ')',   (0, 2): 'mc',  (0, 3): 'm+', (0, 4): 'm-', (0, 5): 'mr',   (0, 6): "AC", (0, 7): "+/-", (0, 8): "%", (0, 9): "÷",
            (1, 0): '2nd', (1, 1): 'x^2', (1, 2): 'x^3', (1, 3): 'x^y', (1, 4): 'e^x', (1, 5): '10^x', (1, 6): "7",  (1, 7): "8",   (1, 8): "9", (1, 9): "x",
            (2, 0): '1/x', (2, 1): '2√x', (2, 2): '3√x', (2, 3): 'y√x', (2, 4): 'ln',  (2, 5): 'log10',(2, 6): "4",  (2, 7): "5",   (2, 8): "6", (2, 9): "-",
            (3, 0): 'x!', (3, 1): 'sin', (3, 2): 'cos', (3, 3): 'tan',  (3, 4): 'e',   (3, 5): 'EE',   (3, 6): "1",  (3, 7): "2",   (3, 8): "3", (3, 9): "+",
            (4, 0): 'Rad', (4, 1): 'sinh', (4, 2): 'cosh', (4, 3): 'tanh',  (4, 4): 'π',   (4, 5): 'Rand', (4, 6): "0",  (4, 7): "",  (4, 8): ".", (4, 9): "=",
        }

        # 그리드 레이아웃에 버튼 추가
        for position, text in button_positions.items():
            if position == (4, 6):
                button = QPushButton("0")
                button.setMinimumSize(100, 50)
                button.clicked.connect(self.button_clicked)
                grid_layout.addWidget(button, 4, 6, 1, 2)  # 1행 2열 크기
            elif text:
                button = QPushButton(text)
                button.setMinimumSize(50, 50)
                button.clicked.connect(self.button_clicked)
                grid_layout.addWidget(button, *position)
            else:
                empty_widget = QWidget()  # 빈칸을 위한 빈 위젯
                grid_layout.addWidget(empty_widget, *position)

        layout.addLayout(grid_layout)
        self.setLayout(layout)
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 500, 300)

    def update_display(self, value):
        self.display.setText(value)

    def button_clicked(self):
        button = self.sender()
        text = button.text()
        current_text = self.display.text().replace(',', '')  # 콤마 제거

        if text.isdigit():  # 숫자 입력
            if current_text == "0":
                self.update_display(text)
            else:
                self.update_display(current_text + text)
        elif text in ['+', '-', 'x', '÷']:  # 산술 연산자
            self.pending_op = text
            self.pending_value = current_text
            self.update_display("0")
        elif text == "=":  # 결과 계산
            result = self.calculate(self.pending_value, self.pending_op, current_text)
            self.update_display("{:,}".format(result))
        elif text == "AC":  # 전체 초기화
            self.update_display("0")
        elif text == "+/-":  # 부호 변경
            if current_text.startswith("-"):
                self.update_display(current_text[1:])
            else:
                self.update_display("-" + current_text)
        elif text == "%":  # 백분율
            value = float(current_text) / 100
            self.update_display(str(value))
        elif text == '(':  # 왼쪽 괄호
            self.update_display(current_text + "(")
        elif text == ')':  # 오른쪽 괄호
            self.update_display(current_text + ")")
        elif text == '1/x':  # 역수
            result = 1 / float(current_text)
            self.update_display(str(result))
        elif text == 'x^2':  # 제곱
            result = math.pow(float(current_text), 2)
            self.update_display(str(result))
        elif text == 'x^3':  # 삼차 제곱
            result = math.pow(float(current_text), 3)
            self.update_display(str(result))
        elif text == 'x^y':  # y 제곱
            # 구현하지 않은 경우 추가로 계산 기능 추가 필요
            pass
        elif text == 'x!':  # 팩토리얼
            result = math.factorial(int(current_text))
            self.update_display(str(result))
        elif text == '2√x':  # 제곱근
            result = math.sqrt(float(current_text))
            self.update_display(str(result))
        elif text == '3√x':  # 세제곱근
            result = math.pow(float(current_text), 1 / 3)
            self.update_display(str(result))
        elif text == 'y√x':  # y 제곱근
            # 추가 계산 기능 필요
            pass
        elif text == 'ln':  # 자연 로그
            result = math.log(float(current_text))
            self.update_display(str(result))
        elif text == 'log10':  # 상용 로그
            result = math.log10(float(current_text))
            self.update_display(str(result))
        elif text == 'sin':  # 사인
            result = math.sin(math.radians(float(current_text)))  # 라디안 변환
            self.update_display(str(result))
        elif text == 'cos':  # 코사인
            result = math.cos(math.radians(float(current_text)))
            self.update_display(str(result))
        elif text == 'tan':  # 탄젠트
            result = math.tan(math.radians(float(current_text)))
            self.update_display(str(result))
        elif text == 'sinh':  # 쌍곡 사인
            result = math.sinh(float(current_text))
            self.update_display(str(result))
        elif text == 'cosh':  # 쌍곡 코사인
            result = math.cosh(float(current_text))
            self.update_display(str(result))
        elif text == 'tanh':  # 쌍곡 탄젠트
            result = math.tanh(float(current_text))
            self.update_display(str(result))
        elif text == 'π':  # 파이
            result = math.pi
            self.update_display(str(result))
        elif text == 'e':  # 자연상수 e
            result = math.e
            self.update_display(str(result))
        elif text == '10^x':  # 10의 x제곱
            result = math.pow(10, float(current_text))
            self.update_display(str(result))
        elif text == 'e^x':  # 자연상수 e의 x제곱
            result = math.exp(float(current_text))
            self.update_display(str(result))
        elif text == 'mc':  # 메모리 초기화
            self.memory = 0
        elif text == 'm+':  # 메모리 더하기
            self.memory += float(current_text)
        elif text == 'm-':  # 메모리 빼기
            self.memory -= float(current_text)
        elif text == 'mr':  # 메모리 리콜
            self.update_display(str(self.memory))
        elif text == 'Rad':  # 라디안 모드
            # 현재 코드에서 특별한 처리 없음
            pass
        elif text == 'Rand':  # 랜덤 숫자
            result = random.random()  # 0과 1 사이의 랜덤 숫자
            self.update_display(int(result))
        else:
            # 기타 버튼에 대한 처리 추가 가능
            pass

    def calculate(self, value1, operator, value2):
        # 연산자를 기반으로 연산 수행
        if operator == "+":
            result = float(value1) + float(value2)
        elif operator == "-":
            result = float(value1) - float(value2)
        elif operator == "x":
            result = float(value1) * float(value2)
        elif operator == "÷":
            result = float(value1) / float(value2)
        else:
            result = 0  # 기본값
        
        return result


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
