import sys

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

# Passing in sys.argv allows us to pass command line args into the app
app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    # toggled = False
    # label = QLabel
    # input = QLineEdit

    # arguments, key-word arguments
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Rubble Rescue")

        layout = QHBoxLayout()
        sidePanelLayout = QVBoxLayout()
    #     self.label = QLabel(self)
    #     self.input = QLineEdit(self)

    #     closeButton = QPushButton("X", self)
    #     closeButton.setText("X")
    #     closeButton.move(80, 80)
    #     closeButton.setMinimumWidth(100)
    #     closeButton.setCheckable(True)
    #     closeButton.clicked.connect(self.closeButtonClicked)

    #     victimButton = QPushButton("Victim", self)
    #     victimButton.setText("Victim")
    #     victimButton.move(80, 50)
    #     victimButton.setMinimumWidth(100)
    #     victimButton.setCheckable(True)
    #     victimButton.clicked.connect(self.victimClicked)
    #     self.input.move(80, 150)
    #     self.input.textChanged.connect(self.label.setText)
    #     self.label.move(80, 100)

    # def closeButtonClicked(self):
    #     exit()
    
    # def victimClicked(self, checked):
    #     self.toggled = checked
    #     print(self.toggled)

# create app's GUI
window = MainWindow()

# show app's GUI
window.showMaximized()

# Start the event loop
app.exec()