from PyQt5.QtWidgets import QApplication
from ui import MainFrame
import sys
import os

if __name__ == '__main__':
    os.system('taskkill /im chromedriver.exe /F')  # kill all chromedriver.exe
    os.system('taskkill /im chrome.exe /F')  # kill all chrome.exe
    app = QApplication(sys.argv)
    mainFrame = MainFrame()
    mainFrame.show()
    sys.exit(app.exec_())


# ---逆轉科技有限公司 開源程式碼---