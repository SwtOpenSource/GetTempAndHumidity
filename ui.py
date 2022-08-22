from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFrame, QWidget
from PyQt5.QtCore import Qt

from thread import ThreadClass


class UiForm(object):

    def __init__(self):
        """ void all variable """
        self.account_label = None
        self.password_label = None
        self.status_info_label = None
        self.account_lineEdit = None
        self.password_lineEdit = None
        self.pushButton = None
        self.thread = None
        self.child_window = None

    def setupUi(self, Form):
        """ setting all windows' ui """
        _translate = QtCore.QCoreApplication.translate
        Form.setObjectName("Form")
        Form.resize(450, 180)
        Form.setWindowTitle(_translate("Form", "UniFi 登入"))
        Form.setWindowIcon(QtGui.QIcon('icon.png'))

        self.account_label = QtWidgets.QLabel(Form)
        self.account_label.setGeometry(QtCore.QRect(20, 5, 51, 61))
        self.account_label.setObjectName("label")

        self.password_label = QtWidgets.QLabel(Form)
        self.password_label.setGeometry(QtCore.QRect(20, 55, 51, 61))
        self.password_label.setObjectName("label")

        self.status_info_label = QtWidgets.QLabel(Form)
        self.status_info_label.setGeometry(QtCore.QRect(100, 70, 293, 28))
        self.status_info_label.setObjectName("label")
        # self.status_info_label.setAlignment(Qt.AlignCenter)

        self.account_lineEdit = QtWidgets.QLineEdit(Form)
        self.account_lineEdit.setGeometry(QtCore.QRect(80, 20, 351, 30))
        self.account_lineEdit.setObjectName("lineEdit")

        self.password_lineEdit = QtWidgets.QLineEdit(Form)
        self.password_lineEdit.setGeometry(QtCore.QRect(80, 70, 351, 30))
        self.password_lineEdit.setObjectName("lineEdit")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(170, 120, 93, 28))
        self.pushButton.setObjectName("pushButton")

        self.labeledit()
        self.lineedit_init()
        self.check_input_func()
        self.buttonedit()

    def button_click(self):
        """ button event """
        account = self.account_lineEdit.text()  # save input account
        password = self.password_lineEdit.text()  # save input password
        self.thread = ThreadClass(account=account, password=password, mainframe=self)
        self.thread.start()
        self.pushButton.setEnabled(False)
        self.show_child_window()

    def buttonedit(self):
        """ edit all button """
        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("Form", "登入"))
        self.pushButton.clicked.connect(self.button_click)  # connect button click event

    def labeledit(self):
        """ edit all label """
        _translate = QtCore.QCoreApplication.translate
        self.account_label.setText(_translate("Form", "帳號："))
        self.password_label.setText(_translate("Form", "密碼："))
        self.status_info_label.setText(_translate("Form", "程式運行中，請勿關閉此視窗"))

    def lineedit_init(self):
        """ edit all input line """
        self.account_lineEdit.setPlaceholderText('請輸入帳號')
        self.password_lineEdit.setPlaceholderText('請輸入密碼')
        self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)  # hide password
        self.account_lineEdit.textChanged.connect(self.check_input_func)
        self.password_lineEdit.textChanged.connect(self.check_input_func)

    def check_input_func(self):
        """ checking account and password are typed """
        if self.account_lineEdit.text() and self.password_lineEdit.text():
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)

    def show_child_window(self):
        """ messagebox windows """
        self.child_window = ChildW()
        self.child_window.show()


class ChildW(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(-60, 100)
        self.setWindowTitle("Loading")

        self.load_label = QtWidgets.QLabel(self)
        self.load_label.setGeometry(QtCore.QRect(20, 5, 160, 100))
        self.load_label.setObjectName("label")

        _translate = QtCore.QCoreApplication.translate
        self.load_label.setAlignment(Qt.AlignCenter)
        self.load_label.setText(_translate("Form", "登入中請稍後..."))


class MainFrame(QFrame, UiForm):
    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent)  # 調用父類把子類對象轉為父類對象
        # 調用介面
        self.setupUi(self)
