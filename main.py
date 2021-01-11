import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.con = sqlite3.connect("coffee.db")
        self.setGeometry(200, 100, 500, 400)

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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
