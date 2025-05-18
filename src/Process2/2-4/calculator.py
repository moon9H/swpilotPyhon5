import sys
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
        self.current_value = None
        self.current_operator = None

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
        grid_layout.setSpacing(0)  # 버튼 간의 여백을 최소화

        # 버튼의 텍스트 및 그리드 위치 설정
        button_positions = {
            (0, 0): "AC", (0, 1): "+/-", (0, 2): "%", (0, 3): "÷",
            (1, 0): "7", (1, 1): "8", (1, 2): "9", (1, 3): "x",
            (2, 0): "4", (2, 1): "5", (2, 2): "6", (2, 3): "-",
            (3, 0): "1", (3, 1): "2", (3, 2): "3", (3, 3): "+",
            (4, 0): "0", (4, 1): "", (4, 2): ".", (4, 3): "=",
        }

        # 그리드 레이아웃에 버튼 추가
        for position, text in button_positions.items():
            if position == (4, 0) or position == (4,1):  # "0" 버튼은 두 칸을 차지
                button = QPushButton("0")
                button.setMinimumSize(100, 50)  # 두 칸을 차지하도록 설정
                button.clicked.connect(self.button_clicked)
                grid_layout.addWidget(button, 4, 0, 1, 2)
            elif text:
                button = QPushButton(text)
                button.setMinimumSize(50, 50)  # 두 칸을 차지하도록 설정
                button.clicked.connect(self.button_clicked)
                grid_layout.addWidget(button, *position)

        # 그리드 레이아웃을 수직 레이아웃에 추가
        layout.addLayout(grid_layout)

        # 전체 레이아웃 설정
        self.setLayout(layout)
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 300, 300)

    def button_clicked(self):
        button = self.sender()  # 클릭된 버튼 가져옴
        text = button.text()

        if text.isdigit():  # 숫자 버튼 클릭
            current_text = self.display.text().replace(',', '')  # 콤마 제거
            new_text = current_text + text  # 숫자 추가

            formatted_text = "{:,}".format(int(new_text))  # 세자리마다 콤마 추가
            self.display.setText(formatted_text)  # 디스플레이 업데이트

        elif text == "+":  # 덧셈
            self.set_operator("+")

        elif text == "-":  # 뺄셈
            self.set_operator("-")

        elif text == "x":  # 곱셈
            self.set_operator("*")

        elif text == "÷":  # 나눗셈
            self.set_operator("/")

        elif text == "=":  # 결과 계산
            self.equal()

        elif text == "AC":  # 초기화
            self.reset()

        elif text == "+/-":  # 부호 변경
            self.negative_positive()

        elif text == "%":  # 퍼센트
            self.percent()

        elif text == ".":  # 소수점
            self.add_decimal()

    def set_operator(self, operator):
        # 디스플레이에 보이는 숫자를 현재 값으로 설정
        self.current_value = int(self.display.text().replace(',', ''))
        self.current_operator = operator
        self.display.clear()  # 디스플레이 초기화

    def equal(self):
        if self.current_operator and self.current_value is not None:
            # 디스플레이의 숫자 가져오기
            new_value = int(self.display.text().replace(',', ''))

            if self.current_operator == "+":
                result = self.current_value + new_value
            elif self.current_operator == "-":
                result = self.current_value - new_value
            elif self.current_operator == "*":
                result = self.current_value * new_value
            elif self.current_operator == "/":
                if new_value == 0:
                    result = "Error"  # 0으로 나누기 방지
                else:
                    result = self.current_value / new_value

            if isinstance(result, int):
                formatted_result = "{:,}".format(result)
                self.display.setText(formatted_result)  # 결과 디스플레이
            else:
                self.display.setText(str(result))  # 오류 메시지 표시

            self.current_value = None  # 연산 후 초기화
            self.current_operator = None

    def reset(self):
        self.display.clear()  # 디스플레이 초기화
        self.current_value = None
        self.current_operator = None  # 내부 상태 초기화

    def negative_positive(self):
        current_text = self.display.text().replace(',', '')
        if current_text:
            number = int(current_text)
            number *= -1  # 부호 변경
            formatted_text = "{:,}".format(number)  # 세자리 콤마
            self.display.setText(formatted_text)  # 디스플레이 업데이트

    def percent(self):
        current_text = self.display.text().replace(',', '')
        if current_text:
            number = int(current_text)
            percent_value = number / 100  # 퍼센트 변환
            self.display.setText(str(percent_value))  # 소수점으로 표시

    def add_decimal(self):
        current_text = self.display.text()
        if "." not in current_text:  # 소수점이 없을 때만 추가
            new_text = current_text + "."
            self.display.setText(new_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())