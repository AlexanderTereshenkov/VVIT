import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton


class Calculator(QWidget):
    def __init__(self):
        self.error = False
        super(Calculator, self).__init__()

        self.vbox = QVBoxLayout(self)
        self.hbox_input = QHBoxLayout()
        self.hbox_first = QHBoxLayout()
        self.hbox_second = QHBoxLayout()
        self.hbox_third = QHBoxLayout()
        self.hbox_fourth = QHBoxLayout()
        self.hbox_result = QHBoxLayout()

        self.vbox.addLayout(self.hbox_input)
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addLayout(self.hbox_second)
        self.vbox.addLayout(self.hbox_third)
        self.vbox.addLayout(self.hbox_fourth)
        self.vbox.addLayout(self.hbox_result)

        self.input = QLineEdit(self)
        self.hbox_input.addWidget(self.input)
        self.clearButton = QPushButton("С", self)
        self.hbox_input.addWidget(self.clearButton)
        self.clearButton.clicked.connect(lambda: self.clear_edit())

        self.b_1 = QPushButton("1", self)
        self.hbox_first.addWidget(self.b_1)

        self.b_2 = QPushButton("2", self)
        self.hbox_first.addWidget(self.b_2)

        self.b_3 = QPushButton("3", self)
        self.hbox_first.addWidget(self.b_3)

        self.b_plus = QPushButton("+", self)
        self.hbox_first.addWidget(self.b_plus)

        self.b_4 = QPushButton("4", self)
        self.hbox_second.addWidget(self.b_4)

        self.b_5 = QPushButton("5", self)
        self.hbox_second.addWidget(self.b_5)

        self.b_6 = QPushButton("6", self)
        self.hbox_second.addWidget(self.b_6)

        self.b_minus = QPushButton("-", self)
        self.hbox_second.addWidget(self.b_minus)

        self.b_7 = QPushButton("7", self)
        self.hbox_third.addWidget(self.b_7)

        self.b_8 = QPushButton("8", self)
        self.hbox_third.addWidget(self.b_8)

        self.b_9 = QPushButton("9", self)
        self.hbox_third.addWidget(self.b_9)

        self.b_multiply = QPushButton("*", self)
        self.hbox_third.addWidget(self.b_multiply)

        self.b_0 = QPushButton("0", self)
        self.hbox_fourth.addWidget(self.b_0)

        self.b_dot = QPushButton(".", self)
        self.hbox_fourth.addWidget(self.b_dot)

        self.b_change = QPushButton("+/-", self)
        self.hbox_fourth.addWidget(self.b_change)

        self.b_divide = QPushButton("/", self)
        self.hbox_fourth.addWidget(self.b_divide)

        self.b_result = QPushButton("=", self)
        self.hbox_result.addWidget(self.b_result)

        self.input.textEdited.connect(lambda: self.text_changed())

        self.b_plus.clicked.connect(lambda: self._operation("+"))
        self.b_minus.clicked.connect(lambda: self._operation("-"))
        self.b_multiply.clicked.connect(lambda: self._operation("*"))
        self.b_divide.clicked.connect(lambda: self._operation("/"))
        self.b_dot.clicked.connect(lambda: self._button("."))
        self.b_change.clicked.connect(lambda: self._button("-"))
        self.b_result.clicked.connect(self._result)
        self.b_1.clicked.connect(lambda: self._button("1"))
        self.b_2.clicked.connect(lambda: self._button("2"))
        self.b_3.clicked.connect(lambda: self._button("3"))
        self.b_4.clicked.connect(lambda: self._button("4"))
        self.b_5.clicked.connect(lambda: self._button("5"))
        self.b_6.clicked.connect(lambda: self._button("6"))
        self.b_7.clicked.connect(lambda: self._button("7"))
        self.b_8.clicked.connect(lambda: self._button("8"))
        self.b_9.clicked.connect(lambda: self._button("9"))
        self.b_0.clicked.connect(lambda: self._button("0"))
        #super().__init__()

    def _button(self, param):
        if self.error:
            self.input.setText("")
            self.error = False
        line = self.input.text()
        if param == "-":
            if "-" not in line:
                if line:
                    self.input.setText("-" + line)
            if "-" in line:
                self.input.setText(line[1:])
        elif param == ".":
            if not line:
                self.input.setText("0" + param)
            else:
                self.input.setText(line + param)
        else:
            self.input.setText(line + param)

    def _operation(self, op):
        if self.input.text() != "":
            if '.' in self.input.text():
                self.num_1 = float(self.input.text())
            else:
                self.num_1 = int(self.input.text())
        self.op = op
        self.input.setText("")

    def _result(self):
        if '.' in self.input.text():
            self.num_2 = float(self.input.text())
        else:
            self.num_2 = int(self.input.text())
        if self.op == "+":
            self.input.setText(str(self.check_result(self.num_1 + self.num_2)))
        if self.op == "-":
            self.input.setText(str(self.check_result(self.num_1 - self.num_2)))
        if self.op == "*":
            self.input.setText(str(self.check_result(self.num_1 * self.num_2)))
        if self.op == "/":
            if self.num_2 == 0:
                self.error = True
                self.input.setText("Ошибка: деление на 0")
            else:
                self.input.setText(str(self.check_result(self.num_1 / self.num_2)))

    def clear_edit(self):
        self.input.setText("")

    def check_result(self, result):
        result = str(result)
        if result[len(result)-2:] == ".0":
            return int(float(result))
        else:
            return result

    def text_changed(self):
        s = self.input.text()
        if s:
            if s[-1] not in '1234567890.':
                self.input.setText(s[:len(s)-1])
            if s[-1] in '+-/*=':
                if s[-1] == "=":
                    self._result()
                else:
                    self._operation(s[-1])

app = QApplication(sys.argv)
win = Calculator()
win.show()
sys.exit(app.exec_())
