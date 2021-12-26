import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget
from sqligther import SQLighter
from PyQt5.QtGui import QIcon
import datetime
import math


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        # Конфигурация окна
        self.setWindowIcon(QIcon('img/icon.png'))
        self.setWindowTitle('Калькулятор с историей вычислений')
        # Подключаем базу данных
        self.lighter = SQLighter('db/calculation_history.db')
        self.update_table()
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
        self.btn_delete.clicked.connect(self.delete_selected_items)

        ## Переменная, в которых хранятся последнее введённое число/результат вычисленного выражения
        self.data = ''
        ## Переменная, в которых хранятся выражение, которое нужно подсчитать
        self.data_eval = ''

    # вычисление факториала
    def real_fact(self, n):
        if n == 0:
            return 1
        return n * self.real_fact(n - 1)

    # функция факториала числа
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

    ## Формируется число, с помощью нажатий кнопок и отображается на дисплее
    def run(self):
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

    # Функция вычисления корня из числа
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
                self.lighter.save_results(self.data_eval, self.data, datetime.datetime.now())
                self.data_eval = str(self.data)
                self.update_table()
                self.table.setText(str(self.data))
            except ZeroDivisionError:
                self.table.setText('can"t be divided by zero')
                self.data = ''
                self.data_eval = ''
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

    # функция синуса
    def sin(self):
        if self.data_eval:
            self.data = str(math.sin(float(self.data_eval)))
            self.table.setText(self.data)
            self.lighter.save_results(f'sin({self.data_eval})', self.data, datetime.datetime.now())
            self.data_eval = str(self.data)
            self.update_table()
            self.result()

    # функция косинуса
    def cos(self):
        if self.data_eval:
            self.data = str(math.cos(float(self.data_eval)))
            self.table.setText(self.data)
            self.lighter.save_results(f'cos({self.data_eval})', self.data, datetime.datetime.now())
            self.data_eval = str(self.data)
            self.update_table()
            self.result()

    # функция тангенса
    def tg(self):
        try:
            if self.data_eval:
                self.data = str(math.tan(float(self.data_eval)))
                self.table.setText(self.data)
                self.lighter.save_results(f'tg({self.data_eval})', self.data, datetime.datetime.now())
                self.data_eval = str(self.data)
                self.update_table()
                self.result()
        except Exception:
            self.table.setText('Error')
            self.data = ''
            self.data_eval = ''

    # функция котангенса
    def ctg(self):
        try:
            if self.data_eval == '0':
                raise ZeroDivisionError
            if self.data_eval:
                self.data = str(math.cos(float(self.data_eval)) / math.sin(float(self.data_eval)))
                self.lighter.save_results(f'ctg({self.data_eval})', self.data, datetime.datetime.now())
                self.data_eval = str(self.data)
                self.table.setText(self.data)
                self.update_table()
                self.result()
        except ZeroDivisionError:
            self.table.setText("This value doesn't exist")
            self.data = ''
            self.data_eval = ''
        except Exception:
            self.table.setText("Error")
            self.data = ''
            self.data_eval = ''

    # убирает один разряд из числа
    def backspace(self):
        if self.data_eval:
            self.data_eval = self.data_eval[:-1]
            self.table.setText(self.data_eval)

    # Переворачивает число, делая его противоположным
    def reverse(self):
        if self.data_eval:
            self.data_eval = str((-(float(self.data_eval))))
            self.table.setText(self.data_eval)

    # Функция для вывода истории вычислений в журнал
    def update_table(self):
        self.tableWidget.setColumnCount(4)
        # Достаём все вычисления из базы данных
        result = self.lighter.show_results()[::-1]
        self.tableWidget.setRowCount(len(result))
        for j, i in enumerate(['Id', 'Expression', 'result', 'time']):
            item = QTableWidgetItem()
            item.setText(i)
            self.tableWidget.setHorizontalHeaderItem(j, item)
            # Настройка размеров каждой колонки
            if j == 0:
                self.tableWidget.setColumnWidth(j, 10)
            elif j == 1:
                self.tableWidget.setColumnWidth(j, 150)
            elif j == 2:
                self.tableWidget.setColumnWidth(j, 130)
            elif j == 3:
                self.tableWidget.setColumnWidth(j, 150)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    # Функция удаления выбранных вычислений из истории
    def delete_selected_items(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        self.lighter.remove_results(ids=ids)
        self.update_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
