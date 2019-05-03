from PyQt5 import QtWidgets, uic

import sys

app = QtWidgets.QApplication([])

win = uic.loadUi("GuiTest.ui")  # specify the location of your .ui file
z
win.show()

sys.exit(app.exec())

