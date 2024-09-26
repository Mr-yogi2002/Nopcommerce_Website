import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from Test_locators.locators import WebXpath
from Test_Excel_functions.excel_functions import all_excel_functions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestNop:
    @pytest.fixture()
    def booting_function(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        excel_file = "C:\\Users\\Admin\\Desktop\\YOGESH\\POMDemo\\Test_Datas\\test_data.xlsx"
        sheet_number = "Sheet1"
        self.s = all_excel_functions(excel_file, sheet_number)
        self.rows = self.s.row_count()
        yield
        self.driver.close()

    def test_login(self, booting_function):
        self.driver.maximize_window()
        self.driver.get(WebXpath.url)
        self.driver.implicitly_wait(20)
        wait = WebDriverWait(self.driver, 20)
        start_row = 2
        last_row = 6

        for row_number in range(start_row, last_row + 1):

            username = self.s.read_data(row_number, 5)
            password = self.s.read_data(row_number, 6)

            menu = wait.until(EC.presence_of_element_located((By.XPATH, WebXpath.login_menu)))
            menu.click()
            # time.sleep(5)
            username_ele = wait.until(EC.presence_of_element_located((By.XPATH, WebXpath().username_input)))
            username_ele.send_keys(username)
            # time.sleep(5)
            pass_ele = wait.until(EC.presence_of_element_located((By.XPATH, WebXpath.password_input)))
            pass_ele.send_keys(password)
            # time.sleep(5)
            login_button = wait.until(EC.presence_of_element_located((By.XPATH, WebXpath().submit_button)))
            login_button.click()
            # time.sleep(5)

            wait.until(EC.presence_of_element_located((By.XPATH, WebXpath.logout)))
            logout_text = self.driver.find_element(By.XPATH, WebXpath.logout).text
            print(logout_text)
            # time.sleep(5)

            if logout_text == 'Log out':
                print("SUCCESS: Logged in the username {a} & {b}".format(a=username, b=password))
                # time.sleep(5)
                self.s.write_data(row_number, 7, "TEST PASS")
                # self.driver.refresh()

                profile_button = wait.until(EC.presence_of_element_located((By.XPATH, WebXpath().login_out_box)))
                profile_button.click()
                # time.sleep(5)
                # wait.until(EC.title_is('Log out'))

            else:
                self.s.write_data(row_number, 7, "TEST FAIL")

                print("FAIL: Login failed with username {a} & {b}".format(a=username, b=password))
                self.driver.refresh()

                wait.until(EC.text_to_be_present_in_element((By.XPATH, WebXpath().register), 'Register'))
