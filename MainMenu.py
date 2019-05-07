import sys
import self as self
from PyQt5.QtWidgets import QApplication,QDialog,QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi


class MainMenu(QDialog):
   # def openWindow:
   #     self.window = QApplication.QMain
    def __init__(self):
        super(MainMenu, self).__init__()
        loadUi('MainMenu.ui',self)
        self.setWindowTitle('Stock Market Prediction')
        #self.SignIn.clicked.connect(self.SignIn_clicked)
        #self.SignUp.clicked.connect(self.SignUp_clicked)
        label = QLabel(self)
        pixmap = QPixmap('logo1.JPG')
        #pixmap.scaled(111, 91)
        label.setGeometry(310,50, 160, 160)
        label.setPixmap(pixmap)



    def SignIn_clicked(self):
        UserName = self.UserName.text()
        Password = self.Password.text()
        print(UserName + ' ' + Password)


    def SignUp_clicked(self):
        self.Password.setText('bla')
        t = self.SignUp.text()
        print(t)


app=QApplication(sys.argv)
widget=MainMenu()
widget.show()
sys.exit(app.exec_())