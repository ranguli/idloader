import sys
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets


class Slots:
    # TODO: I don't know that making these static methods is the best practice
    @staticmethod
    def on_open_action():
        print("open sesame!")

class Sidebar(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super(Sidebar, self).__init__(*args, **kwargs)
        #self.setGeometry(QtCore.QRect(380, 50, 524, 685))

        sidebar = QtWidgets.QComboBox()
        self.grid = QtWidgets.QGridLayout(self)
        #sidebar.setLayout(self.grid)

        screenshot_label = QtWidgets.QLabel()
        screenshot = QtGui.QPixmap("screen.jpg")
        screenshot_label.setPixmap(screenshot)

        description = QtWidgets.QTextBrowser()

        # Define how we want to shape our buttons
        fixed = QtWidgets.QSizePolicy.Fixed
        minimum = QtWidgets.QSizePolicy.Minimum
        sizePolicy = QtWidgets.QSizePolicy(minimum, fixed)

        self.download_button = QtWidgets.QPushButton()
        self.download_button.setSizePolicy(sizePolicy)
        self.download_button.setIcon(QtGui.QIcon("icons/drive-download"))

        self.uninstall_button = QtWidgets.QPushButton()
        self.uninstall_button.setSizePolicy(sizePolicy)
        self.uninstall_button.setIcon(QtGui.QIcon("icons/wooden-box--minus"))

        self.install_button = QtWidgets.QPushButton()
        self.install_button.setSizePolicy(sizePolicy)
        self.install_button.setIcon(QtGui.QIcon("icons/wooden-box--plus"))

        self.play_button = QtWidgets.QToolButton()
        self.play_button.setSizePolicy(sizePolicy)
        self.play_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.play_button.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)

        self.grid.addWidget(screenshot_label, 0, 0, 1, 2)
        self.grid.addWidget(description, 1, 0, 1, 2)
        
        # Align the four buttons into a grid with equal size
        self.grid.addWidget(self.download_button, 2, 0, 1, 1)
        self.grid.addWidget(self.play_button, 3, 0, 1, 1)
        self.grid.addWidget(self.install_button, 2, 1, 1, 1)
        self.grid.addWidget(self.uninstall_button, 3, 1, 1, 1)


class Toolbar(QtWidgets.QToolBar):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)

        self.setMovable(False)
        self.setFloatable(False)

class Menubar(QtWidgets.QMenuBar):
    def __init__(self, *args, **kwargs):
        super(Menubar, self).__init__(*args, **kwargs)

        file_menu = self.addMenu("&File")
        open_action = QtWidgets.QAction(QtGui.QIcon("icons/wooden-box--plus.png"), "&Install mod from file", self)
        open_action.setStatusTip("Open a file")
        file_menu.addAction(open_action)
        
        edit_menu = self.addMenu("&Edit")
        add_engine_action = QtWidgets.QAction(QtGui.QIcon("icons/processor.png"), "&Add engine", self)
        add_engine_action.setStatusTip("Open a file")
        edit_menu.addAction(add_engine_action)
        
        help_menu = self.addMenu("&Help")
        docs_action = QtWidgets.QAction(QtGui.QIcon("icons/book.png"), "&Documentation", self)
        donate_action = QtWidgets.QAction(QtGui.QIcon("icons/jar-open.png"), "&Donate", self)
        about_action = QtWidgets.QAction(QtGui.QIcon("icons/question.png"), "&About", self)
        help_menu.addAction(docs_action)
        help_menu.addAction(donate_action)
        help_menu.addAction(about_action)

        #open_action.triggered.connect(Slots.on_open_action())


class SearchBar(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SearchBar, self).__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout(self)

        search_icon = QtWidgets.QLabel()
        search_icon.setPixmap(QtGui.QPixmap("icons/magnifier-left.png"))
        search_field = QtWidgets.QLineEdit()
        search_field.setPlaceholderText("Search...")
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(sizePolicy)

        self.layout.addWidget(search_icon)
        self.layout.addWidget(search_field)

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data


    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d")
            elif isinstance(value, str):
                return value
            #return value

        if role == Qt.DecorationRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, datetime):
                return QtGui.QIcon("icons/calendar.png")
            elif isinstance(value, bool):
                if value:
                    return QtGui.QIcon("icons/tick.png")
            
            if index.column() == 2:
                icon = QtGui.QIcon() 
                icon.addPixmap(QtGui.QPixmap("icons/star-small.png"))
                return icon 

    def rowCount(self, index):
        # The length of the outer list
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class Table(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.setSizePolicy(sizePolicy)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setShowGrid(False)

        self.setColumnCount(6)
        # This should dynamically be the number of rows in the sql database
        self.setRowCount(1)

        self.column_name = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(0, self.column_name)
        
        self.column_title = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(1, self.column_title)
        
        self.column_author = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(2, self.column_author)
        
        self.column_release_date = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(3, self.column_release_date)
        
        self.column_rating = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(4, self.column_rating)
        
        self.column_downloaded = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(5, self.column_downloaded)
        
        self.row_item = QtWidgets.QTableWidgetItem()
        self.setVerticalHeaderItem(0, self.row_item)
        self.verticalHeader().setVisible(False)


class Tabs(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        super(Tabs, self).__init__(*args, **kwargs)

        self.setDocumentMode(True)
        self.setMovable(False)


        quake_icon = QtGui.QIcon()
        quake_icon.addPixmap(QtGui.QPixmap("quake128x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.quake_table = Table()
        self.addTab(self.quake_table, quake_icon, "Quake")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.setSizePolicy(sizePolicy)

        self.setCurrentIndex(0)

class Color(QtWidgets.QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)
        
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        self.setPalette(palette)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("idloader")
        layout = QtWidgets.QGridLayout()
    

        self.toolbar = Toolbar()
        self.addToolBar(self.toolbar)

        self.menubar = Menubar()
        self.setMenuBar(self.menubar)
        
        self.searchbar = SearchBar()
        layout.addWidget(self.searchbar, 0, 0)#, 1, 1)#, 1, 1)

        self.sidebar = Sidebar()
        layout.addWidget(self.sidebar, 0, 2, 3, 1)
        
        self.tabs = Tabs()
        layout.addWidget(self.tabs, 1, 0)
        
        window_contents = QtWidgets.QWidget()
        window_contents.setLayout(layout)
        
        self.setCentralWidget(window_contents)
        self.retranslate(MainWindow)


    def retranslate(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.sidebar.setTitle(_translate("MainWindow", "Details"))
        self.sidebar.download_button.setText(_translate("MainWindow", "Download"))
        self.sidebar.play_button.setText(_translate("MainWindow", "Play"))
        self.sidebar.install_button.setText(_translate("MainWindow", "Install"))
        self.sidebar.uninstall_button.setText(_translate("MainWindow", "Uninstall"))

        # for tab in tabs:
            # get the table on that tab
                # do this:

        self.tabs.quake_table.column_name.setText(_translate("MainWindow", "Name"))
        self.tabs.quake_table.column_title.setText(_translate("MainWindow", "Title"))
        self.tabs.quake_table.column_author.setText(_translate("MainWindow", "Author"))
        self.tabs.quake_table.column_release_date.setText(_translate("MainWindow", "Release"))
        self.tabs.quake_table.column_rating.setText(_translate("MainWindow", "Rating"))
        self.tabs.quake_table.column_downloaded.setText(_translate("MainWindow", "Downloaded"))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
