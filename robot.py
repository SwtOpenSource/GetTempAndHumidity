from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PyQt5 import QtCore
from typing import Union
from datetime import datetime
import time
import csv
import os


def all_device_url() -> Union[list[str], bool]:
    """ get url device from .txt """
    if os.path.isfile("deviceURL.txt"):
        with open("deviceURL.txt", "r") as id_file:
            id_list = id_file.readlines()
        return id_list

    else:
        with open('deviceURL.txt', 'w') as device_id_file:
            device_url = ""  # default empty
            device_id_file.write(device_url)
        return False


def time_interval():
    """ get time interval from .txt """
    if os.path.isfile("time(min).txt"):
        with open('time(min).txt', 'r') as timeinterval_file:
            timeinterval = timeinterval_file.read()
    else:
        with open('time(min).txt', 'w') as timeinterval_file:
            timeinterval = "5"  # default
            timeinterval_file.write(timeinterval)
    return time.sleep(float(timeinterval) * 60)


class Robot:
    def __init__(self, mainframe):
        self.mainframe = mainframe
        self._translate = QtCore.QCoreApplication.translate
        self.unifi_url = "https://unifi.ui.com"
        self.device_url_list = all_device_url()
        self.driver = None

    def set(self):
        """ chrome setting """
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 啟動Headless 無介面
        chrome_options.add_argument('--disable-gpu')  # 關閉GPU 避免某些系統或是網頁出錯
        try:
            self.driver = webdriver.Chrome('./chromedriver', options=chrome_options)
            return True
        except Exception as e:
            print(e)
            print("Chromdriver error")
            return False

    def get_unifi_url(self) -> bool:
        """ go to unifi and check internet"""
        try:
            self.driver.get(self.unifi_url)
            return True
        except Exception as e:
            print(e)
            print("網路無連線")
            return False

    def login_in(self, account: str, password: str) -> bool:
        """ login to unifi """
        self.driver.find_element(By.NAME, "username").send_keys(account)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.NAME, "password").submit()
        time.sleep(5)  # 登入後暫停5秒，確定完成登入
        try:
            self.driver.find_element(By.ID, "unifi-portal-styles")
            return True
        except Exception as e:
            print(e)
            print("登入失敗")
            return False

    def login_result(self, status: bool):
        """ show login result on GUI"""
        if status:
            self.mainframe_display_status(True)
            self.mainframe.child_window.load_label.setText(
                self._translate("Form", "登入成功"))
            time.sleep(5)  # 5秒後自動關閉登入成功視窗
            self.mainframe.child_window.close()
        else:
            self.mainframe.child_window.load_label.setText(
                self._translate("Form", "帳號或密碼有誤"))
            self.mainframe.pushButton.setEnabled(True)

    def create_page(self):
        """ create web page by each device"""
        for i in range(len(self.device_url_list)):
            self.driver.execute_script(f'window.open()')
            self.driver.switch_to.window(self.driver.window_handles[i + 1])
            self.driver.get(self.device_url_list[i])
            self.driver.implicitly_wait(3)

    def start(self) -> Union[str, bool]:
        """ start get temperature and humidity data """
        try:
            if not self.device_url_list:
                self.mainframe.status_info_label.setText(
                    self._translate("Form", "未輸入URL，請先輸入後再試"))
                return "URL Error"
            for i in range(len(self.device_url_list)):
                self.get_data_and_save(i + 1)
            time_interval()
            return True
        except Exception as e:
            print(e)
            return False

    def mainframe_display_status(self, status: int, which: str = None):
        """ display status on GUI after check internet """
        self.mainframe.account_label.close()
        self.mainframe.password_label.close()
        self.mainframe.account_lineEdit.close()
        self.mainframe.password_lineEdit.close()
        self.mainframe.pushButton.close()
        if which == "chromedriver":
            if not status:
                self.mainframe.child_window.close()
                self.mainframe.status_info_label.setText(
                    self._translate("Form", "請 安 裝 正 確 Chromedriver.exe"))
        if which == "internet":
            if not status:
                self.mainframe.child_window.close()
                self.mainframe.status_info_label.setText(
                    self._translate("Form", "未連接上網路，關閉後再試一次"))
        self.mainframe.status_info_label.show()

    def get_data_and_save(self, page: int):
        """ get data and save it as .csv in observation"""
        self.driver.switch_to.window(self.driver.window_handles[page])
        data_list = self.driver.find_elements(By.CSS_SELECTOR,
                                              value="span[class='SensorReadingsState__ChipText-sc-1ygwv1j-2 cFlQgU']")
        humidity = None
        temperature = None
        for i in range(len(data_list)):
            if "%" in data_list[i].text:
                humidity = data_list[i].text
            if "°C" in data_list[i].text:
                temperature = data_list[i].text
        location = self.driver.find_element(By.CSS_SELECTOR,
                                            value="span[class='text-base__bIyDk3C7 text-size-caption__bIyDk3C7 "
                                                  "text-light-header__bIyDk3C7 truncate__bIyDk3C7 "
                                                  "text-weight-normal__bIyDk3C7 "
                                                  "primaryHeading__bIyDk3C7 undefined']").text
        if not humidity or not temperature:
            location = "裝置不存在"
            humidity = "請檢查URL，最後10碼為"
            temperature = self.driver.current_url[-10:]

        observation_path = os.getcwd() + "/observation"
        if not os.path.isdir(observation_path):
            os.makedirs(observation_path)
        filename = f"{os.getcwd()}/observation/{str(datetime.now().date())}.csv"
        if not os.path.isfile(filename):
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['時間', '地點', '濕度', '溫度'])

        with open(filename, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([now, location, humidity, temperature])

    def refresh(self, account: str, password: str):
        """ clean all cookies and refresh by login again """
        try:
            for i in range(len(self.device_url_list)):
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.delete_all_cookies()
            self.driver.get(self.unifi_url)
            self.driver.find_element(By.NAME, "username").send_keys(account)
            self.driver.find_element(By.NAME, "password").send_keys(password)
            self.driver.find_element(By.NAME, "password").submit()
            time.sleep(60)  # 預設重整後暫停60秒，以免連續重整
        except Exception as e:
            print(e)
