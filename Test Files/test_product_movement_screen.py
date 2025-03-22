from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import allure
import time
import pytest
import excel_utils_functions
import logging

@allure.severity(allure.severity_level.NORMAL)
class TestApp:
    def setup_class(self):
        self.file_path = "E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\Inventory_Test_Data.xlsx"
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    @allure.severity(allure.severity_level.MINOR)
    def test_menu_page(self):
        try:
            self.driver.get('http://127.0.0.1:5000/home')
            self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\home_page.png")
            select_product = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//li[@class='nav-item dropdown'][3]")))
            ActionChains(self.driver).move_to_element(select_product).perform()
            time.sleep(3)
            try:
                add_option = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//a[contains(@href,'/productmove')][normalize-space()='ADD']")))
                add_click = ActionChains(self.driver).move_to_element(add_option).perform()
                time.sleep(3)
                ActionChains(self.driver).click(add_click).perform()
                time.sleep(3)
                print("ADD Options",add_option.text)
            except StaleElementReferenceException as e:
                self.driver.refresh()
                print("pandiyaraj",self.driver.current_url)
                cur_url = self.driver.current_url
                self.test_productmove_add()
                print("Current URL",cur_url)
            time.sleep(3)
        except Exception as e:
            print(f"Error io :{e}")

    @allure.severity(allure.severity_level.CRITICAL)
    def test_productmove_add(self):
        try:
            current_url=self.driver.current_url
            print("In Coming")
            self.driver.refresh()
            self.driver.get(current_url)
            self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\product_movement_page.png")
            rows = excel_utils_functions.row_count(self.file_path, 'Product Add Data')

            print("Row Count:", rows)
            for row in range(2, rows+1):
                product_id = excel_utils_functions.read_data(self.file_path,"Product Move", row, 1)
                date = excel_utils_functions.read_data(self.file_path,"Product Move", row, 2)
                date_cnvrt = date.strftime('%d-%m-%Y')
                print(date_cnvrt)
                from_location = excel_utils_functions.read_data(self.file_path,"Product Move", row, 3)
                to_location = excel_utils_functions.read_data(self.file_path,"Product Move", row, 4)
                qty = excel_utils_functions.read_data(self.file_path,"Product Move", row, 5)
                expected_result = excel_utils_functions.read_data(self.file_path,"Product Move", row, 6)
                # web element
                self.driver.find_element(By.ID,"product_id").send_keys(product_id)
                self.driver.find_element(By.NAME,"date").send_keys(date_cnvrt)
                self.driver.find_element(By.NAME,"from_location").send_keys(from_location)
                self.driver.find_element(By.NAME,"to_location").send_keys(to_location)
                self.driver.find_element(By.NAME,"qty").send_keys(qty)
                self.driver.find_element(By.XPATH,"//input[@type='submit']").click()
                time.sleep(3)
                # element = self.driver.find_element(By.XPATH,"/html/body/div[1]/h4[1]")
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/h4[1]")))
                # ActionChains(self.driver).scroll_to_element(element).perform()
                time.sleep(3)
                print("Message:", element.text)
                self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\product_move_msg.png")
                time.sleep(3)
        except Exception as e:
            print(f"Error :{e}")
    

    @allure.severity(allure.severity_level.MINOR)
    def test_get_location_to_update(self):
        self.driver.get('http://127.0.0.1:5000/productmove_update_query')
        cols = self.driver.find_elements(By.XPATH,"//table//tbody//tr[1]//th")
        print(len(cols))
        rows = self.driver.find_elements(By.XPATH,"//table//tr")
        print(len(rows))
        
        # length of rows and columns
        row_len = len(rows)
        col_len = len(cols)

        for i in range(2, row_len+1):
            # for j in range(1,col_len+1):
            product_move_update = f"//table//tr[{i}]//td[5]"
            edit_btn = f"//table//tr[{i}]//td[6]//a"
            try:
                product_move_qty_update = self.driver.find_element(By.XPATH,product_move_update).text
                print("Product QTY",product_move_qty_update)
                edit_data = self.driver.find_element(By.XPATH,edit_btn)
                edit_data.click()
                expected_url = f"http://127.0.0.1:5000/product_move_update/{product_move_qty_update}"
                print("Navigate to the next page",expected_url)
                WebDriverWait(self.driver, 10).until(EC.url_changes(expected_url))
                print("Navigation success..")
                time.sleep(3)
                self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\movemoent_update_screen.png")
                
                # update the location desc
                self.driver.find_element(By.NAME,"qty").clear()
                location_desc_update = self.driver.find_element(By.NAME, "qty")
                location_desc_update.send_keys("10")
                self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\qty_update.png")
                self.driver.find_element(By.XPATH,"//input[@value='UPDATE']").click()
                time.sleep(3)

                main_page = self.driver.current_url
                print(main_page)
                time.sleep(3)
                update_msg = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/h4[1]")))
                print("Message:", update_msg.text)
                self.driver.implicitly_wait(10)
                self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\product_move_update_screen.png")
                time.sleep(3)
                
            except Exception as e:
                print(f"Error : {e}")

    @allure.severity(allure.severity_level.BLOCKER)
    def test_location_delete(self):
        rows_count = excel_utils_functions.row_count(self.file_path, 'Product Move')
        self.driver.get("http://127.0.0.1:5000/productmove_delete_query")
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
                delete_btn = f"//table//tr[{i}]//td[6]//a"
                try:
                    data = self.driver.find_element(By.XPATH,product_xpath).text
                    si_data = self.driver.find_element(By.XPATH,delete_btn)
                    print("Final Data",data)
                    print("Single Data",si_data.text)
                    for row in range(2, rows_count+1):
                        product_id = excel_utils_functions.read_data(self.file_path,"Product Move", row, 1)
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
            self.driver.get("http://127.0.0.1:5000/productmove_data_view")
            self.driver.implicitly_wait(10)
            self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\product_movement_report.png")
            time.sleep(3)
        except Exception as e:
            print(f"Error: {e}")