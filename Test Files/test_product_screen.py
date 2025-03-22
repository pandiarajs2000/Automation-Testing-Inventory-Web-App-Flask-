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
        self.new_product_id = input("Enter the Product ID")
        self.new_product_desc = input("Enter the Product Description")
        self.file_path = "E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\Inventory_Test_Data.xlsx"
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    @allure.severity(allure.severity_level.MINOR)
    def test_menu_page(self):
        try:
            self.driver.get('http://127.0.0.1:5000/home')
            self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\home_page.png")
            select_product = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//li[@class='nav-item dropdown'][1]")))
            ActionChains(self.driver).move_to_element(select_product).perform()
            time.sleep(3)
            try:
                add_option = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//a[contains(@href,'/product_add')][normalize-space()='ADD']")))
                add_click = ActionChains(self.driver).move_to_element(add_option).perform()
                time.sleep(3)
                ActionChains(self.driver).click(add_click).perform()
                time.sleep(3)
                print("ADD Options",add_option.text)
            except StaleElementReferenceException as e:
                self.driver.refresh()
                print("pandiyaraj",self.driver.current_url)
                cur_url = self.driver.current_url
                self.test_product_add(cur_url)
                print("Current URL",cur_url)
            time.sleep(3)
        except Exception as e:
            print(f"Error io :{e}")

    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_add(self):
        try:
            current_url=self.driver.current_url
            print("In Coming")
            self.driver.refresh()
            print("Product Add URL : ",self.driver.get(current_url))
            self.driver.get(current_url)
            self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\product_page.png")
            rows = excel_utils_functions.row_count(self.file_path, 'Product Add Data')
            
            new_data = self.new_product_id
            new_desc = self.new_product_desc

            print("Row Count:", rows)
            for row in range(2, rows+1):
                product_id = excel_utils_functions.read_data(self.file_path,"Product Add Data", row, 1)
                # product_desc = excel_utils_functions.read_data(self.file_path,"Product Add Data", row, 2)
                expected_result = excel_utils_functions.read_data(self.file_path,"Product Add Data", row, 3)
                # web element
                data = self.driver.find_element(By.NAME,"product_id")
                data.send_keys(new_data)
                print(data.text)
                self.driver.find_element(By.NAME,"product_desc").send_keys(new_desc)
                self.driver.find_element(By.XPATH,"//input[@type='submit']").click()
                time.sleep(3)
                element = self.driver.find_element(By.XPATH,"/html/body/div[1]/h4[1]")
                print("Message:", element.text)

                if product_id != new_data and new_data != expected_result:
                    print("Test Passed")
                    # self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\test_pass.png")
                    self.driver.implicitly_wait(10)
                    self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\product_test_pass.png")
                    time.sleep(3)
                    excel_utils_functions.write_data(self.file_path, "Product Add Data",row, 4,"Failed")
                else:
                    print("Test Failed")
                    self.driver.implicitly_wait(10)
                    self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\product_test_fail.png")
                    time.sleep(3)
                    excel_utils_functions.write_data(self.file_path, "Product Add Data",row, 4,"Passed")

            time.sleep(3)
        except StaleElementReferenceException as e:
            print(f"Error:{e}")

    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_the_product(self):
        pytest.skip("Skip the function..")

    @allure.severity(allure.severity_level.MINOR)
    def test_get_product_to_update(self):
        try:
            self.driver.get('http://127.0.0.1:5000/product_update_view')
            cols = self.driver.find_elements(By.XPATH,"//table//tbody//tr[1]//th")
            print(len(cols))
            rows = self.driver.find_elements(By.XPATH,"//table//tr")
            print(len(rows))
            
            # length of rows and columns
            row_len = len(rows)
            col_len = len(cols)

            for i in range(2, row_len+1):
                for j in range(1,col_len+1):
                    x_path = f"//table//tr[{i}]//td[{j}]"
                    data = self.driver.find_element(By.XPATH,x_path).text
                    print("Final Data",data)
            try:
                exact_row = f"//table//tr[2]//td[3]//a"
                row_xpath = self.driver.find_element(By.XPATH,exact_row)
                ActionChains(self.driver).scroll_to_element(row_xpath).perform()
                # ("Edit URL",self.driver.current_url)
                href_data = row_xpath.get_attribute("href")

                if href_data:
                    self.test_set_data_update(href_data)
                    print("href data",href_data)
                else:
                    print("Error : href_data not found..")
            except Exception as e:
                print(f"Error retrieving href_data: {e}")
        except Exception as e:
            print(f"Error in test_get_product_to_update: {e}")
            

    def test_set_data_update(self):
        try:
            self.driver.current_url
            # self.driver.get(href_data)
            page_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/h1[1]"))).text
            print("Tilte",page_name)
            
            id_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/form/label[1]"))).text
            print("ID Name",id_name)
            desc = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/form/label[2]"))).text
            print(desc)

            product_id = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//input[@name='product_id']")))
            print("Product ID",product_id.get_attribute("value"))

            product_desc = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//input[@name='product_desc']")))
            print("Product Description",product_desc.get_attribute("value"))

            # clear the current value
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//input[@name='product_desc']"))).clear()

            # update the data
            data_send = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//input[@name='product_desc']")))
            data_send.send_keys('LCD Module Gells')
            print("New Data",data_send.get_attribute('value'))
            

            # update button 
            update_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//input[@type='submit']")))
            update_btn.click()
            current_url = self.driver.current_url
            print("Current URL",current_url)
            self.test_get_updates_msg()
        except Exception as e:
            print(f"Error : {e}")

    def test_get_updates_msg(self):
        try:
            data_display = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h4[1]")))
            if data_display.is_displayed():
                ActionChains(self.driver).scroll_to_element(data_display).perform()
                print(data_display.text)
            else:
                print("Element is not displayed.")
        except Exception as e:
            print(f"Error : This element Already Updated... if you want update the element kindly update the text in code..")
            back_to_home = self.driver.find_element(By.XPATH,"/html/body/div[1]/a/button")
            ActionChains(self.driver).move_to_element(back_to_home).perform()
            time.sleep(3)
            back_to_home.click()
            time.sleep(3)

    @allure.severity(allure.severity_level.BLOCKER)
    def test_product_delete(self):
        row_counts = excel_utils_functions.row_count(self.file_path, "Demo Data")
        print("Rows:", row_counts)
        self.driver.get("http://127.0.0.1:5000/product_delete_view")
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
    def test_product_report_view(self):
        try:
            self.driver.get("http://127.0.0.1:5000/product_add_data_view")
            self.driver.implicitly_wait(10)
            self.driver.get_screenshot_as_file("E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\screenshots\sample.png")
            time.sleep(3)
        except Exception as e:
            print(f"Error: {e}")