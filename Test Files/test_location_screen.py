from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import allure
import time
import pytest
import excel_utils_functions
import logging

@allure.severity(allure.severity_level.NORMAL)
class TestApp:
    def setup_class(self):
        self.new_product_id = input("Enter the Location ID")
        self.new_product_desc = input("Enter the Location Description")
        self.update_product_desc = input("Enter the Location Desc for update :\n")
        self.file_path = "E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\Inventory_Test_Data.xlsx"
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    @allure.severity(allure.severity_level.MINOR)
    def test_menu_page(self):
        try:
            self.driver.get('http://127.0.0.1:5000/home')
            self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\home_page.png")
            select_product = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//li[@class='nav-item dropdown'][2]")))
            ActionChains(self.driver).move_to_element(select_product).perform()
            time.sleep(3)
            try:
                add_option = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//a[contains(@href,'/location_page')][normalize-space()='ADD']")))
                add_click = ActionChains(self.driver).move_to_element(add_option).perform()
                time.sleep(3)
                ActionChains(self.driver).click(add_click).perform()
                time.sleep(3)
                print("ADD Options",add_option.text)
            except StaleElementReferenceException as e:
                self.driver.refresh()
                print("pandiyaraj",self.driver.current_url)
                cur_url = self.driver.current_url
                self.test_location_add()
                print("Current URL",cur_url)
            time.sleep(3)
        except Exception as e:
            print(f"Error io :{e}")

    @allure.severity(allure.severity_level.CRITICAL)
    def test_location_add(self):
        try:
            current_url=self.driver.current_url
            print("current url", current_url)
            self.driver.refresh()
            print("Product Add URL : ",self.driver.get(current_url))
            self.driver.get(current_url)
            self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\product_page.png")
            rows = excel_utils_functions.row_count(self.file_path, 'Locations Data')
            
            new_data = self.new_product_id
            new_desc = self.new_product_desc

            print("Row Count:", rows)
            for row in range(2, rows+1):
                product_id = excel_utils_functions.read_data(self.file_path,"Locations Data", row, 1)
                # product_desc = excel_utils_functions.read_data(self.file_path,"Locations Data", row, 2)
                expected_result = excel_utils_functions.read_data(self.file_path,"Locations Data", row, 3)
                # web element
                data = self.driver.find_element(By.NAME,"location_id")
                data.send_keys(new_data)
                print(data.text)
                self.driver.find_element(By.NAME,"location_desc").send_keys(new_desc)
                self.driver.find_element(By.XPATH,"//input[@type='submit']").click()
                time.sleep(3)
                element = self.driver.find_element(By.XPATH,"/html/body/div[1]/h4[1]")
                print("Message:", element.text)

                if product_id != new_data and new_data != expected_result:
                    print("Test Passed")
                    # self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\test_pass.png")
                    self.driver.implicitly_wait(10)
                    self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\location_test_pass.png")
                    time.sleep(3)
                    excel_utils_functions.write_data(self.file_path, "Locations Data",row, 4,"Failed")
                else:
                    print("Test Failed")
                    self.driver.implicitly_wait(10)
                    self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\locations_test_fail.png")
                    time.sleep(3)
                    excel_utils_functions.write_data(self.file_path, "Locations Data",row, 4,"Passed")

            time.sleep(3)
        except StaleElementReferenceException as e:
            print(f"Error:{e}")

    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_the_product(self):
        pytest.skip("Skip the function..")

    @allure.severity(allure.severity_level.MINOR)
    def test_get_location_to_update(self):
            self.driver.get('http://127.0.0.1:5000/location_add_update')
            cols = self.driver.find_elements(By.XPATH,"//table//tbody//tr[1]//th")
            print(len(cols))
            rows = self.driver.find_elements(By.XPATH,"//table//tr")
            print(len(rows))
            
            # length of rows and columns
            row_len = len(rows)
            col_len = len(cols)

            for i in range(2, row_len+1):
                # for j in range(1,col_len+1):
                location_xpath = f"//table//tr[{i}]//td[1]"
                edit_btn = f"//table//tr[{i}]//td[3]//a"
                try:
                    location_element = self.driver.find_element(By.XPATH,location_xpath).text
                    edit_data = self.driver.find_element(By.XPATH,edit_btn)
                    edit_data.click()
                    expected_url = f"http://127.0.0.1:5000/location_update/{location_element}"
                    print("Navigate to the next page",expected_url)
                    WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))
                    print("Navigation success..")
                    
                    # update the location desc
                    location_desc_update = self.driver.find_element(By.NAME, "location_desc")
                    location_desc_update.send_keys(self.update_product_desc)
                    self.driver.find_element(By.XPATH,"//input[@type='submit']").click()

                    current_page = self.driver.current_url
                    time.sleep(3)
                    update_msg = self.driver.find_element(By.XPATH,"/html/body/div[1]/h4[1]")
                    print("Message:", update_msg.text)
                    self.driver.implicitly_wait(10)
                    self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\location_update_screen.png")
                    time.sleep(3)

                    
                except Exception as e:
                    print(f"Error : {e}")

    @allure.severity(allure.severity_level.BLOCKER)
    def test_location_delete(self):
        row_counts = excel_utils_functions.row_count(self.file_path, "Demo Data")
        print("Rows:", row_counts)
        self.driver.get("http://127.0.0.1:5000/location_add_delete_query")
        print(row_counts)
        self.driver.refresh()
        self.driver.delete_all_cookies
        cols = self.driver.find_elements(By.XPATH,"//table//tbody//tr[1]//th")
        print(len(cols))
        rows = self.driver.find_elements(By.XPATH,"//table//tr")
        print(len(rows))
        
        # length of rows and columns
        row_len = len(rows)
        col_len = len(cols)

        for i in range(2, row_len+1):
            for j in range(1,col_len+1):
                product_xpath = f"//table//tr[{i}]//td[{j}]"
                delete_btn = f"//table//tr[{i}]//td[3]//a"
                try:
                    data = self.driver.find_element(By.XPATH,product_xpath).text
                    si_data = self.driver.find_element(By.XPATH,delete_btn)
                    print("Final Data",data)
                    print("Single Data",si_data.text)
                    for row in range(2, row_counts+1):
                        product_id = excel_utils_functions.read_data(self.file_path,"Demo Data", row, 1)
                        print("Product ID",product_id)
                        if data == product_id:
                            print("Conditions Meet")
                            del_btn = self.driver.find_element(By.XPATH,delete_btn)
                            del_btn.click()
                            time.sleep(3)
                            try:
                                success_message = self.driver.find_element(By.XPATH, "//h4[1]").text
                                print("Success Message:", success_message)
                            except NoSuchElementException:
                                print(f"Product {data} deleted, but no success message found.")
                except Exception as e:
                    print(f"Error : {e}")

    @allure.severity(allure.severity_level.NORMAL)
    def test_location_report_view(self):
        try:
            self.driver.get("http://127.0.0.1:5000/location_data_view")
            self.driver.implicitly_wait(10)
            self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\location_report.png")
            time.sleep(3)
        except Exception as e:
            print(f"Error: {e}")