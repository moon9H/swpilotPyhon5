# 과정 2 - (문제3) "계산기의 제작"

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLineEdit
)
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone Style Calculator")
        self.setFixedSize(320, 500)
        self.setStyleSheet("""
            background-color: black;
            border-radius: 100px;
        """)
        self.expression = ""  # 내부 수식 문자열
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # 출력창
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet(
        "font-size: 36px; padding: 20px; background-color: black; color: white; border: none;"
    )
        main_layout.addWidget(self.display)

        # 버튼 그리드
        grid = QGridLayout()
        main_layout.addLayout(grid)

        # 버튼 텍스트 구성
        buttons = [
            ['⌫', '+/-', '%', '÷'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['🖩', '0', '.', '=']
        ]

        # 버튼 생성 및 배치
        for row, row_values in enumerate(buttons):
            col_offset = 0
            for col, btn_text in enumerate(row_values):
                button = QPushButton(btn_text)
                button.setFixedSize(70, 70)
                button.setStyleSheet("font-size: 20px; border-radius: 35px;")

                if btn_text in ['÷', 'x', '-', '+', '=']:
                    button.setStyleSheet("background-color: orange; color: white; font-size: 20px; border-radius: 35px;")
                elif btn_text in ['⌫', '+/-', '%']:
                    button.setStyleSheet("background-color: #a5a5a5; color: black; font-size: 20px; border-radius: 35px;")
                else:
                    button.setStyleSheet("background-color: #333333; color: white; font-size: 20px; border-radius: 35px;")

                grid.addWidget(button, row, col, 1, 1)
                button.clicked.connect(lambda _, text=btn_text: self.on_button_click(text))

    def format_number(self, number_str):
        if '.' in number_str:
            integer_part, decimal_part = number_str.split('.')
            formatted = "{:,}".format(int(integer_part)) + '.' + decimal_part
        else:
            formatted = "{:,}".format(int(number_str))
        return formatted

    def on_button_click(self, value):
        if value in '0123456789':
            self.expression += value
            parts = list(filter(None, self.expression.replace('+',' ').replace('-',' ').replace('*',' ').replace('/',' ').split(' ')))
            last_number = parts[-1] if parts else self.expression
            try:
                formatted = self.format_number(last_number)
                display_expr = self.expression[:-len(last_number)] + formatted
                self.display.setText(display_expr)
            except:
                self.display.setText(self.expression)
        elif value == '.':
            if not self.expression or not self.expression[-1].isdigit():
                return  # 점은 숫자 뒤에만 허용
            self.expression += '.'
            self.display.setText(self.display.text() + '.')
        elif value == '⌫':
            self.expression = self.expression[:-1]
            self.display.setText(self.display.text()[:-1])
        # (보너스 과제) - 4칙연산 구현 코드
        elif value in ['+', '-', 'x', '÷']:
            if self.expression and self.expression[-1] not in '+-*/':
                op = {'x': '*', '÷': '/'}[value] if value in 'x÷' else value
                self.expression += op
                self.display.setText(self.display.text() + value)
        elif value == '=':
            try:
                result = str(eval(self.expression))
                self.expression = result
                self.display.setText(self.format_number(result))
            except:
                self.display.setText("Error")
                self.expression = ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())