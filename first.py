from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import randrange
import sys


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Ui.ui", self)
        self.setGeometry(200, 100, 500, 400)
        self.pushButton.clicked.connect(self.update)

    def paintEvent(self, event):
            painter = QPainter(self)
            painter.setPen(QColor(255, 204, 0))
            painter.setBrush(QColor(255, 204, 0))
            radius = randrange(10, 50)
            if radius > 500 - radius:
                painter.drawEllipse(QPoint(randrange(500 - radius, radius),
                                           randrange(400 - radius, radius)), radius, radius)
            else:
                painter.drawEllipse(QPoint(randrange(radius, 500 - radius),
                                           randrange(radius, 400 - radius)), radius, radius)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
