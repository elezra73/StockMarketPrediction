import sys
import self as self
from PyQt5.QtWidgets import QApplication,QDialog,QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from MainMenu import widget


class Login(QDialog):
    print('tqwe')
    def __init__(self):
        super(Login, self).__init__()
        loadUi('Login.ui',self)
        self.setWindowTitle('Stock Market Prediction')
        self.SignIn.clicked.connect(self.SignIn_clicked)
        self.SignUp.clicked.connect(self.SignUp_clicked)
        label = QLabel(self)
        pixmap = QPixmap('logo1.JPG')
        label.setGeometry(310,50, 160, 160)
        label.setPixmap(pixmap)
        print('test')


    def openWindow(self):
        print('test')
        self.window = QtWidgets.QDialog()
        self.ui = widget()
        self.ui.setupUi(self.window)
        self.window.show()


    def SignIn_clicked(self):
        UserName = self.UserName.text()
        Password = self.Password.text()
        print(UserName + ' ' + Password)
       # self.openWindow(self)

    def SignUp_clicked(self):
        self.Password.setText('bla')
        t = self.SignUp.text()
        print(t)



app=QApplication(sys.argv)
widget=Login()
widget.show()
sys.exit(app.exec_())