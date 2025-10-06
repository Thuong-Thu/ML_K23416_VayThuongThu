from MainWindowEx import MainWindowEx
import sys
from PyQt6 import QtWidgets

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowEx()
        self.ui.setupUi(self)
        self.ui.connectMySQL()
        self.ui.selectAllStudent()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())