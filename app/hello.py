import sys

# import QApplication and all the required widgets
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

# create instance of QApplication
# you should crate your app instance before you create any GUI object in PyQt
app = QApplication([])

# create app's GUI
window = QWidget()
window.setWindowTitle("Test App")
window.setGeometry(100, 100, 280, 80)
helloMsg = QLabel("<h1>Hello, World!</h1>", parent=window)
helloMsg.move(60, 15)

# show app's GUI
window.show()

# run app's event loop
sys.exit(app.exec())

