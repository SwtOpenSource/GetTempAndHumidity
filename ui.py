from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFrame, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from thread import ThreadClass
import os


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
        self.child_window = ChildW()

    def setupUi(self, Form):
        """ setting all windows' ui """
        _translate = QtCore.QCoreApplication.translate
        Form.setObjectName("Form")
        Form.resize(450, 180)
        Form.setFixedSize(Form.width(), Form.height())
        Form.setWindowTitle(_translate("Form", "UniFi 登入"))
        Form.setWindowIcon(QtGui.QIcon('iconswt.png'))

        logo = QtWidgets.QLabel(Form)
        logo.setGeometry(QtCore.QRect(290, 110, 193, 58))
        pixmap = QPixmap("swt.png")
        logo.setPixmap(pixmap)

        self.account_label = QtWidgets.QLabel(Form)
        self.account_label.setGeometry(QtCore.QRect(20, 5, 51, 61))
        self.account_label.setObjectName("label")

        self.password_label = QtWidgets.QLabel(Form)
        self.password_label.setGeometry(QtCore.QRect(20, 55, 51, 61))
        self.password_label.setObjectName("label")

        self.status_info_label = QtWidgets.QLabel(Form)
        self.status_info_label.setGeometry(QtCore.QRect(100, 70, 293, 28))
        self.status_info_label.setObjectName("label")

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
        self.child_window.show()


class NoticeW(QWidget):
    def __init__(self, mainframe):
        """ void variable """
        super().__init__()
        self.mainframe = mainframe
        self.status = True
        self.notice_label = QtWidgets.QLabel(self)
        self.notice_label_2 = QtWidgets.QLabel(self)
        self.runButton = QtWidgets.QPushButton(self)
        self.unrunButton = QtWidgets.QPushButton(self)
        self.noticeUi()

    def noticeUi(self):
        """ setting notice windows' ui """
        self.resize(355, 150)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("提醒")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.notice_label.setGeometry(QtCore.QRect(5, 0, 350, 100))
        self.notice_label.setObjectName("label")

        self.notice_label_2.setGeometry(QtCore.QRect(5, 25, 350, 100))
        self.notice_label_2.setObjectName("label")

        self.runButton.setGeometry(QtCore.QRect(50, 100, 93, 28))
        self.runButton.setObjectName("pushButton")

        self.unrunButton.setGeometry(QtCore.QRect(210, 100, 93, 28))
        self.unrunButton.setObjectName("pushButton")

        self.edit_item()

    def edit_item(self):
        """ edit notice item """
        _translate = QtCore.QCoreApplication.translate
        self.notice_label.setAlignment(Qt.AlignCenter)
        self.notice_label.setText(_translate("Form", "使用前，會先將所有Chrome瀏覽器關閉"))
        self.notice_label_2.setAlignment(Qt.AlignCenter)
        self.notice_label_2.setText(_translate("Form", "請先確認完畢，再按下「執行」按鈕"))
        self.runButton.setText(_translate("Form", "執行"))
        self.runButton.clicked.connect(self.button_click)
        self.unrunButton.setText(_translate("Form", "不執行"))
        self.unrunButton.clicked.connect(self.closeEvent)

    def button_click(self):
        """ button event """
        os.system('taskkill /im chromedriver.exe /F')  # kill all chromedriver.exe
        os.system('taskkill /im chrome.exe /F')  # kill all chrome.exe
        self.mainframe.show()
        self.hide()
        self.status = False

    def closeEvent(self, event):
        """ button event """
        self.close()


class ChildW(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(-60, 100)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("Loading")
        self.setWindowIcon(QtGui.QIcon('iconswt.png'))

        self.load_label = QtWidgets.QLabel(self)
        self.load_label.setGeometry(QtCore.QRect(10, 5, 160, 100))
        self.load_label.setObjectName("label")

        _translate = QtCore.QCoreApplication.translate
        self.load_label.setAlignment(Qt.AlignCenter)
        self.load_label.setText(_translate("Form", "登入中請稍後..."))


class MainFrame(QFrame, UiForm):
    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent)  # 調用父類把子類對象轉為父類對象
        # 調用介面
        self.setupUi(self)
