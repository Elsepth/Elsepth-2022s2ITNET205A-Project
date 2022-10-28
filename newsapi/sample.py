from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSlot
import sys

data = {'author': ['VnExpress'], 'title': ['Trung Quốc tạo nam châm xung điện mạnh nhất thế giới'], 'url': ['https://vnexpress.net/trung-quoc-tao-nam-cham-xung-dien-manh-nhat-the-gioi-4516998.html'], 'publishedAt': ['2022-09-29T12:00:00Z']}
 
class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
 
    def setData(self): 
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)
 
def main(args):
    app = QApplication(args)
    table = TableView(data, 1, 4)
    table.show()
    sys.exit(app.exec())
 
if __name__=="__main__":
    main(sys.argv)