import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QButtonGroup
import math


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        # ## Подключаем цифры
        self.buttonGroup_digits = QButtonGroup()
        self.buttonGroup_binary = QButtonGroup()
        for i, j in enumerate(
                [self.btn_0, self.btn_1, self.btn_2, self.btn_3, self.btn_4, self.btn_5, self.btn_6, self.btn_7,
                 self.btn_8, self.btn_9]):
            self.buttonGroup_digits.addButton(j, i)
        for i, j in enumerate([self.btn_plus, self.btn_inc, self.btn_del]):
            self.buttonGroup_binary.addButton(j, i)
        [i.clicked.connect(self.run) for i in self.buttonGroup_digits.buttons()]
        # ## Подключаем бинарные операции (+,-,*,/)
        [i.clicked.connect(self.calc) for i in self.buttonGroup_binary.buttons()]
        # ## Подключаем точку
        self.btn_dot.clicked.connect(self.run)
        # ## Подключаем кнопку равно
        self.btn_eq.clicked.connect(self.result)
        # ## Подключаем кнопку очистки
        self.btn_clear.clicked.connect(self.clear)
        # ## Подключаем унарные операции
        self.btn_sqrt.clicked.connect(self.sqrt)
        self.btn_fact.clicked.connect(self.fact)
        # Подключаем тригонометрические функции
        self.btn_cos.clicked.connect(self.cos)
        self.btn_sin.clicked.connect(self.sin)
        self.btn_tan.clicked.connect(self.tg)
        self.btn_cotg.clicked.connect(self.ctg)
        # Подключаем остальные функции
        self.btn_back.clicked.connect(self.backspace)
        self.btn_reverse.clicked.connect(self.reverse)

        ## Переменная, в которых хранятся последнее введённое число/результат вычисленного выражения
        self.data = ''
        ## Переменная, в которых хранятся выражение, которое нужно подсчитать
        self.data_eval = ''

    def real_fact(self, n):
        if n == 0:
            return 1
        return n * self.real_fact(n - 1)

    def fact(self):
        try:
            if self.data_eval:
                self.data_eval = str(self.real_fact(float(self.data_eval)))
                self.table.setText(self.data_eval)
                self.result()
        except Exception:
            self.table.setText("Error")

    ## Сброс всех данных, очистка экрана
    def clear(self):
        self.data = ''
        self.data_eval = ''
        self.table.setText('0')

    def run(self):
        ## Формируется число, с помощью нажатий кнопок и отображается на дисплее
        try:
            if self.sender().text() == '.':
                if '.' in self.data:
                    return
            if self.data != '0' or (self.data == '0' and self.sender().text() == '.'):
                self.data = self.data + self.sender().text()
                self.data_eval = self.data_eval + self.sender().text()
                self.table.setText(self.data)
            else:
                self.data = self.sender().text()
                self.data_eval = self.sender().text()
                self.table.setText(self.data)
        except Exception:
            self.table.setText('Error')

    def sqrt(self):
        if self.data_eval:
            self.data_eval += '**0.5'
            self.result()

    def result(self):
        ## Происходит попытка вычисления выражения, в случае попытки деления на 0, выводится ошибка
        try:
            float(self.data_eval)
        except:
            try:
                self.data = eval(self.data_eval)
                self.data_eval = str(self.data)
                self.table.setText(str(self.data))
            except Exception:
                self.table.setText('Error')
        self.data = ''

    def calc(self):
        ## Происходит вычисление текущего выражения и дописывается новый знак. Если последним был уже знак действия, то он менятся.
        if self.data_eval:
            self.result()
            if (self.data_eval[-1] not in ['+', '-', '/', '*']):
                self.data_eval += self.sender().text()
            else:
                self.data_eval = self.data_eval[0:len(self.data_eval) - 1] + self.sender().text()
            self.data_eval = self.data_eval.replace('^', '**')

    def sin(self):
        if self.data_eval:
            self.data_eval = str(math.sin(float(self.data_eval)))
            self.table.setText(self.data_eval)
            self.result()

    def cos(self):
        if self.data_eval:
            self.data_eval = str(math.cos(float(self.data_eval)))
            self.table.setText(self.data_eval)
            self.result()

    def tg(self):
        try:
            if self.data_eval:
                self.data_eval = str(math.tan(float(self.data_eval)))
                self.table.setText(self.data_eval)
                self.result()
        except Exception:
            self.talbe.setText('Error')

    def ctg(self):
        try:
            if self.data_eval:
                self.data_eval = str(math.cos(float(self.data_eval)) / math.sin(float(self.data_eval)))
                self.table.setText(self.data_eval)
                self.result()
        except Exception:
            self.table.setText("Error")

    def backspace(self):
        if self.data_eval:
            self.data_eval = self.data_eval[:-1]
            self.table.setText(self.data_eval)

    def reverse(self):
        if self.data_eval:
            self.data_eval = str((-(float(self.data_eval))))
            self.table.setText(self.data_eval)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
