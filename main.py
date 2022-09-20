from PyQt5.QtWidgets import QApplication
from ui import MainFrame, NoticeW
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainFrame = NoticeW(MainFrame())
    mainFrame.show()
    sys.exit(app.exec_())


# ---逆轉科技有限公司 開源軟體---
