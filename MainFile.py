import cx_Oracle

from Qt.test import *
from Qt.SecondWindow import *

from PyQt5.QtWidgets import *
import sys

from MplForWidget import MyMplCanavas
from TimeMatplotlib import PlotGraph
# from anotation_2 import PlotGraph

import datetime as dt

CONST_COUNT_CURRENCY = 1400

'''
url = 'https://api.coincap.io/v2/assets?limit=%d' % CONST_COUNT_CURRENCY
response = requests.request('GET', url)
data = response.json()
'''


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.window = None

        dsnStr = cx_Oracle.makedsn(host="localhost", port="1521", sid="dborcl")
        con = cx_Oracle.connect(user="user1", password="123", dsn=dsnStr)
        cur = con.cursor()
        cur.execute("SELECT ID, RANK FROM CRYPTO_CURRENCY_DATA ORDER BY RANK")
        result = cur.fetchall()

        for i in result:
            print((100-len(str(i[0]))))
            item = '{0}'.format(str(i[0]))
            self.listWidget.addItem(item)

        self.listWidget.itemClicked.connect(self.clicked_ChooseCurrency)

    def clicked_ChooseCurrency(self, item):
        self.window = SecondWindow(item.text())
        self.window.pushButton.setText('Update')
        self.window.show()
        # QMessageBox.information(self, "ListWidget", "You clicked: " + item.text())


class SecondWindow(QMainWindow, Ui_Dialog):
    def __init__(self, coin):
        super().__init__()
        self.setupUi(self)
        self.coin = coin
        self.fig = PlotGraph(self.coin)
        self.companovka_for_mpl = QVBoxLayout(self.widget)
        self.canavas = MyMplCanavas(self.fig)
        self.companovka_for_mpl.addWidget(self.canavas)

        self.pushButton.clicked.connect(self.newGraph)

    def newGraph(self):
        self.close()
        self.companovka_for_mpl.removeWidget(self.canavas)
        self.companovka_for_mpl.update()

        if self.lineEdit.text() == '--' and self.lineEdit_2.text() == '--':
            self.canavas = MyMplCanavas(PlotGraph(self.coin))
        elif self.lineEdit.text() != '--' and self.lineEdit_2.text() == '--':
            self.canavas = MyMplCanavas(PlotGraph(self.coin,
                                                  dt.datetime.strptime('%s' % self.lineEdit.text(), "%d-%m-%Y").timestamp(),
                                                  0))
        elif self.lineEdit.text() == '--' and self.lineEdit_2.text() != '--':
            self.canavas = MyMplCanavas(PlotGraph(self.coin,
                                                  0,
                                                  dt.datetime.strptime('%s' % self.lineEdit_2.text(), "%d-%m-%Y").timestamp()))
        else:
            self.canavas = MyMplCanavas(PlotGraph(self.coin,
                                                  dt.datetime.strptime('%s' % self.lineEdit.text(),
                                                                       "%d-%m-%Y").timestamp(),
                                                  dt.datetime.strptime('%s' % self.lineEdit_2.text(),
                                                                       "%d-%m-%Y").timestamp()))

        self.companovka_for_mpl.addWidget(self.canavas)
        self.companovka_for_mpl.update()
        self.show()


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
