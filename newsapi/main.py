# main.py

import sys
from logging import Logger

from news import SearchNews

from PyQt6.QtCore import Qt, QAbstractTableModel

from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QTableWidgetItem, QTableWidget, QTableView, QPushButton, QLabel, QMainWindow, QLineEdit, QComboBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Latest News")
        self.setFixedWidth(1200)
        self.setFixedHeight(400)

        widget = MainWidget()
        self.setCentralWidget(widget)


class HLayout(QHBoxLayout):
    def __init__(self, alignment=None, *args):
        super().__init__()
        self.setAlignment(
            alignment if alignment else Qt.AlignmentFlag.AlignLeft)
        for w in args:
            self.addWidget(w)


class Title(QVBoxLayout):
    def __init__(self,):
        super().__init__()
        titleMsg = QLabel("Latest News")
        self.addLayout(HLayout(Qt.AlignmentFlag.AlignCenter, titleMsg))


class SearchForm(QVBoxLayout):
    def __init__(self, parent, result):
        super().__init__()
        self.result = result
        self.parent = parent
        lblSearch = QLabel("Text Search: ")
        self.searchBox = QLineEdit()
        self.searchBox.textChanged.connect(self._data_update)
        self.addLayout(HLayout(None, lblSearch, self.searchBox))
        lblSort = QLabel("Sort by: ")
        self.sortField = QComboBox()
        self.sortField.addItem("author")
        self.sortField.addItem("title")
        self.sortField.addItem("publishAt")
        self.addLayout(HLayout(None, lblSort, self.sortField))
        self.searchButton = QPushButton("Search")
        self.searchButton.setEnabled(False)
        self.searchButton.clicked.connect(self._search_news)
        self.addLayout(
            HLayout(Qt.AlignmentFlag.AlignCenter, self.searchButton))

    def _data_update(self):
        if "" == self.searchBox.text():
            self.searchButton.setEnabled(False)
        else:
            self.searchButton.setEnabled(True)

    def _search_news(self):
        search_news = SearchNews(self.searchBox.text(), self.sortField.itemText(
            self.sortField.currentIndex()), "2022-09-28")
        self.results = search_news.search()
        self._display()
        # self._display_table()

    def _display_table(self):
        table_cols = list(self.results['articles'][0].keys(
        )) if self.results['articles'] else []
        table_data = [[*item.values()] for item in self.results['articles']
                      ] if self.results['articles'] else []

    def _display(self):
        table_cols = list(self.results['articles'][0].keys(
        )) if self.results['articles'] else []
        data = [{key: [
            item[key] for item in self.results['articles']]} for key in table_cols]
        table_data = {k: v for d in data for k, v in d.items()}
        remove_keys = ["content", "urlToImage",
                       "description", "source"] if table_data else []
        for key in remove_keys:
            table_data.pop(key)
        print(table_data)
        tableView = TableView(
            table_data, len(self.results['articles']), len(table_cols)-len(remove_keys))
        self.result.getTable().close()
        self.result.setTable(tableView)
        # self.result.setTable(tableView)
        # self.parent.addWidget(tableView)
        # tableView.show()


class ResultTable(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.table = TableView({}, 1, 4)
        self.addWidget(self.table)

    def getTable(self):
        return self.table

    def setTable(self, tableView):
        self.addWidget(tableView)
        self.table = tableView


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addStretch()
        self.setLayout(self.layout)
        self.layout.addLayout(Title())
        result = ResultTable()
        search = SearchForm(self.layout, result)
        self.layout.addLayout(search)
        self.layout.addLayout(result)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addStretch()


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


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
