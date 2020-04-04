from PyQt5.QtWidgets import QApplication, QWidget, QTableView, QAbstractItemView, QVBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore
import sqlalchemy as db
import os

engine = db.create_engine('sqlite:///demo.db?check_same_thread=False', echo=True)

# 2. Creates demo table
connection = engine.connect()
metadata = db.MetaData()
demoTable = db.Table('demo', metadata,
            db.Column('code', db.String(255), nullable=False),
            db.Column('decription', db.String(255), nullable=False),
            db.Column('uom', db.String(255), nullable=False)
            )

metadata.create_all(engine) 

# 3. Creates demo data
query = db.insert(demoTable) 
values_list = [
    {'code':'058176', 'decription':'01', 'uom':'rb1705,rb1710'},
]
ResultProxy = connection.execute(query,values_list)

class DemoWindow(QWidget):
    def __init__(self, header, *args):
        QWidget.__init__(self, *args)
        self.setWindowTitle("Demo QTableView")

        self.table_model = DemoTableModel(self, header)
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_view)
        self.setLayout(layout)

class DemoTableModel(QAbstractTableModel):

    def __init__(self, parent, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        # 5. fetch data
        results = connection.execute(db.select([demoTable])).fetchall()

        self._data = results
        self.header = header

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._data[0])

    def data(self, index, role):
        # 5. populate data
        if not index.isValid():
            return None
        if (role == Qt.DisplayRole):
            value = self._data[index.row()][index.column()]
            #if isinstance(value, datetime):
            #    return value.strftime("%Y-%m-%d")
            #elif isinstance(value, str):
            #    return value
            #return self._data[index.row()][index.column()]

            return value
        else:
            return QVariant()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

if __name__ == '__main__':
    app = QApplication([])
    header = ['Name', 'Title', 'Author', "Release", "Rating", "Downloaded"]
    win = DemoWindow(header)
    win.show()
    app.exec_()
