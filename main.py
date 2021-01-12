import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem, QMainWindow, QWidget


class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.pushButton.clicked.connect(self.add_coffee)
        self.table = ex.table
        self.id = ex.con.cursor().execute("SELECT * FROM coffee").fetchall()[-1][0] + 1

    def add_coffee(self):
        if not self.lineEdit or not self.lineEdit_2 or not self.lineEdit_3 \
                or not self.lineEdit_4 or not self.lineEdit_5 or not self.lineEdit_6:
            self.label_7.setText('Неверно заполнена форма')
        try:
            cur = ex.con.cursor()
            cur.execute(f"INSERT INTO coffee VALUES({self.id}, '{self.lineEdit.text()}', '{self.lineEdit_2.text()}', "
                        f"'{self.lineEdit_3.text()}', '{self.lineEdit_4.text()}', {float(self.lineEdit_5.text())},"
                        f"{float(self.lineEdit_6.text())})")
            self.id += 1
            cur = ex.con.cursor()
            result = cur.execute("SELECT * FROM coffee").fetchall()
            self.table.setRowCount(len(result))
            self.table.setColumnCount(len(result[0]))
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))
            self.table.setHorizontalHeaderLabels(
                ['ИД', 'Название фильма', 'Год выпуска', 'Жанр', 'Продолжительность'])
            self.table.resizeColumnsToContents()
            ex.con.commit()
            self.hide()
        except ValueError:
            self.label_7.setText('Неверно заполнена форма')


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.titles = ['id', 'name', 'roasting_degree', 'type',
                       'taste', 'price', 'volume']

        self.con = sqlite3.connect("coffee.db")
        self.setGeometry(200, 100, 500, 400)

        self.pushButton.clicked.connect(self.add_coffee)
        self.pushButton_2.clicked.connect(self.save_coffee)

        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.table.setRowCount(len(result))
        self.table.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        self.table.setHorizontalHeaderLabels(['ИД', 'Название', 'Степень обжарки', 'Молотый/в зёрнах',
                                              'Описание вкуса', 'Цена', 'Масса упаковки, гр'])
        self.table.resizeColumnsToContents()

    def add_coffee(self):
        self.window = SecondWindow()
        self.window.show()

    def save_coffee(self):
        cur = self.con.cursor()
        for i in range(self.table.rowCount()):
            que = "UPDATE coffee SET "
            for j in range(self.table.columnCount()):
                if j != 0:
                    if j != 6:
                        que += f"{self.titles[j]} = '{self.table.item(i, j).text()}', "
                    else:
                        que += f"{self.titles[j]} = '{self.table.item(i, j).text()}' "
                else:
                    d = self.table.item(i, j).text()
            que += f"WHERE id = {d}"
            cur.execute(que)
        self.con.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

