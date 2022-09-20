from PyQt5 import QtCore
from robot import Robot


class ThreadClass(QtCore.QThread):
    def __init__(self, account: str, password: str, mainframe, parent=None):
        super(ThreadClass, self).__init__(parent)
        self.account = account
        self.password = password
        self.mainframe = mainframe
        self.robot = Robot(self.mainframe)

    def run(self):
        """ web crawler """
        # check chromedriver version
        chromedriver_result = self.robot.set()
        if not chromedriver_result:
            self.robot.mainframe_display_status(False, which="chromedriver")
            return

        # check internet
        internet_result = self.robot.get_unifi_url()
        if not internet_result:
            self.robot.mainframe_display_status(False, which="internet")
            return

        # check login result
        login_result = self.robot.login_in(account=self.account, password=self.password)
        if login_result:
            self.robot.login_result(True)
        else:
            self.robot.login_result(False)
            return
        self.robot.create_page()
        self.get_data()

    def get_data(self):
        while True:
            # make sure token isn't expired
            status = self.robot.start()
            if status == "URL Error":
                return
            if not status:
                self.robot.refresh(account=self.account, password=self.password)
                self.robot.create_page()
