from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtSql import *

from PyQt5 import QtGui


class TableModel(QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super(TableModel, self).__init__(*args, **kwargs)


if __name__ == "__main__":

    db = QtSql.QSqlDatabase.addDatabase("QPSQL")

    model = TableModel()
    model.setTable("employee")
    model.setEditStrategy(TableModel.OnManualSubmit)
    model.select()
    model.removeColumn(0) # don't show the ID
    model.setHeaderData(0, Qt.Horizontal, model.tr("Name"))
    model.setHeaderData(1, Qt.Horizontal, model.tr("Salary"))

    app = QtWidgets.QApplication([])
    view = QtWidgets.QTableView()
    view.setModel(model)
    view.show()
    app.exec_()
