#!/usr/bin/env python3

'''
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Item(QtWidgets.QWidget):
    def setupUi(self, Item):
        super(Ui_Item, self).__init__(parent)
'''

import sys

import basc_py4chan

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import *

from ui_MainWindow import *
from ui_Item import *

boards = basc_py4chan.get_all_boards()

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self._loadBoards()
        self.listView_2.itemClicked.connect(self.listwidgetclicked)

        #item = QListWidgetItem(self.listWidget_2)
        #self.listWidget_2.addItem(item)

        #row = Ui_Item()
        #item.setSizeHint(row.sizeHint())
        
        #self.listWidget_2.setItemWidget(item, row)

    def _updateView(self):
        self.spinBox.setMaximum(self.board.page_count)
        self.label_2.setText(str(self.board.page_count))

        self.listWidget_2.clear()

        page = self.spinBox.value()

        for i in self.board.get_threads(page):
            item = QListWidgetItem(self.listWidget_2)
            self.listWidget_2.addItem(item)

            row = Ui_Item()
            item.setSizeHint(row.sizeHint())
            row.setTitle(i.topic.subject)
            row.setThumbnail(list(i.thumbs())[0])
            row.setContent(i.topic.text_comment)
            row.setId(i.topic.post_id)

            self.listWidget_2.setItemWidget(item, row)

    def _loadBoards(self):
        lst = self.listView_2

        data = ['/{}/ - {} - {}'.format(i.name, i.title, 'SFW' if i.is_worksafe else 'NSFW' ) for i in boards]

        lst.clear()
        lst.addItems(data)

    def listwidgetclicked(self, item):
        print('!!! click {}'.format(item.text()))
        if item.text().startswith('/'):
            board_name=item.text().split(' - ')[0].replace('/', '')
            self.board = basc_py4chan.get_boards([board_name])[0]

            self._updateView()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
