from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import time

class AppTest:
    def __init__(self):
        self.driver = webdriver.Chrome()
    # global driver 
    # driver = webdriver.Chrome()
    def element_access(self):
        try:
            self.driver.get('http://127.0.0.1:5000/home')
            # select_drop = WebDriverWait(self.driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//li[@class='nav-item dropdown']")))
            # for selects in select_drop:
            #     print("Menu Options",selects.text)
            #     select_text_strip = selects.text.strip()
            #     print("Select Text Strip :",select_text_strip)
            #     print("PRODUCT" in select_text_strip)

            select_product = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//li[@class='nav-item dropdown'][1]")))
            ActionChains(self.driver).move_to_element(select_product).perform()
            time.sleep(3)

            add_option = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//a[contains(@href,'/product_add')][normalize-space()='ADD']")))
            add_click = ActionChains(self.driver).move_to_element(add_option).perform()
            time.sleep(3)
            ActionChains(self.driver).click(add_click).perform()
            time.sleep(3)
            print("ADD Options",add_option.text)

            self.driver.maximize_window()
            time.sleep(20)
        except Exception as e:
            print(f"Error :{e}")
        finally:
            self.driver.quit()
    
      # product add page
    def product_add(self):
        try:
            self.driver.refresh()
            # self.driver.get(current_url)
            self.driver.get("http://127.0.0.1:5000/product_add")
            # print(current_url)
            self.driver.find_element(By.NAME,"product_id").send_keys("Moto G85")
            self.driver.find_element(By.NAME,"product_desc").send_keys("Moto G85 12 GB Ram, 256 GB Storage")
            self.driver.find_element(By.XPATH,"//input[@type='submit']").click()
            time.sleep(3)
            element = self.driver.find_element(By.XPATH,"/html/body/div[1]/h4[1]")
            print("Message:", element.text)
            self.driver.find_element(By.XPATH,"//button[@type='button']").click()
            ActionChains(self.driver).scroll_by_amount(0, 1000).perform()
            time.sleep(4)
            self.driver.maximize_window()
            time.sleep(5)
        except StaleElementReferenceException as e:
            self.driver.refresh()
            print(f"Error :{e}")
        # finally:
        #     driver.find_element(By.XPATH,"//button[@type='button']").click()
        #     ActionChains(driver).scroll_by_amount(0, 1000).perform()
        #     time.sleep(4)
        #     driver.close()

    # product update page
    def get_product_to_update(self):
        try:
            self.driver.get('http://127.0.0.1:5000/product_update_view')
            cols = self.driver.find_elements(By.XPATH,"//table//tbody//tr[1]//th")
            print(len(cols))
            rows = self.driver.find_elements(By.XPATH,"//table//tr")
            print(len(rows))
            # # print the column text
            # for col in cols:
            #     print("Columns",col.text)
            
            # # print the row text
            # for row in rows:
            #     print("Rows",row.text)
            #     print("0th element")
            # # ActionChains(self.driver).scroll_by_amount(0,500).perform()
            
            # # length of rows and columns
            row_len = len(rows)
            col_len = len(cols)
            # print("Row Length :",row_len)
            # print("COlumn Length :",col_len)

            for i in range(2, row_len+1):
                for j in range(1,col_len+1):
                    # print("Rows",i)
                    # print("Cols",j)
                    x_path = f"//table//tr[{i}]//td[{j}]"
                     # btn_path = f"//table//tr[{i}]//td[{j}]//a"
                    data = self.driver.find_element(By.XPATH,x_path).text
                     # link_data = self.driver.find_element(By.XPATH,btn_path).text
                    print("Final Data",data)
                    # print("Link Text Data",link_data)
            
            try:
                exact_row = f"//table//tr[21]//td[3]//a"
                row_xpath = self.driver.find_element(By.XPATH,exact_row)
                ActionChains(self.driver).scroll_to_element(row_xpath).perform()
                href_data = row_xpath.get_attribute("href")
                print("href data",href_data)
                time.sleep(2)
                self.set_data_update(href_data)
            except Exception as e:
                print(f"Error : {e}")
            
            self.driver.maximize_window()
            time.sleep(3)   
        except Exception as e:
            print(f'Error:{e}')
    
    def set_data_update(self,new_page):
        # print(new_page)
        try:
            web_driver = self.driver.get(new_page)
            print("webpage",web_driver)
            # ActionChains(self.driver).key_down(Keys.CONTROL).click(web_driver).perform()
            # ActionChains(self.driver).context_click(web_driver).perform() -> not working
            
            page_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/h1[1]"))).text
            print(page_name)
            
            id_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/form/label[1]"))).text
            print(id_name)
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
            data_send.send_keys('Samsung Galaxy M21')
            print("New Data",data_send.get_attribute('value'))
            

            # update button 
            update_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//input[@type='submit']")))
            update_btn.click()
            current_url = self.driver.current_url
            print("Current URL",current_url)
            self.get_updates_msg()
        except Exception as e:
            print(f"Error : {e}")

    # back to current page
    def get_updates_msg(self):
        # print("Current Page",new_current_pg)
        try:
            update_msg_text = self.driver.find_element(By.XPATH,"//h4[1]")
            data_display = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h4[1]")))
            if data_display.is_displayed():
                ActionChains(self.driver).scroll_to_element(data_display).perform()
                print(data_display.text)
            else:
                print("Element is not displayed.")
            # print("Update Message :", update_msg_text.text)
            # update_view_page = update_msg_text.get_attribute('href')
            # print(update_view_page)
        except Exception as e:
            print(f"Error : This element Already Updated... if you want update the element kindly update the text in code..")
        finally:
            back_to_home = self.driver.find_element(By.XPATH,"//button[@class='btn1']")
            ActionChains(self.driver).move_to_element(back_to_home).perform()
            time.sleep(3)
            back_to_home.click()
            # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='btn1']"))).click()
            time.sleep(3)
    
    def product_delete(self):
        try:
            self.driver.get("http://127.0.0.1:5000/product_delete_view")
            cols = self.driver.find_elements(By.XPATH,"//table//tbody//tr[1]//th")
            print(len(cols))
            rows = self.driver.find_elements(By.XPATH,"//table//tr")
            print(len(rows))
            row_len = len(rows)
            col_len = len(cols)
            for i in range(2, row_len+1):
                for j in range(1,col_len+1):
                    x_path = f"//table//tr[{i}]//td[{j}]"
                    data = self.driver.find_element(By.XPATH,x_path).text
                    print("Final Data",data)
                try:
                    exact_row = f"//table//tr[21]//td[3]//a"
                    row_xpath = self.driver.find_element(By.XPATH,exact_row)
                    if row_xpath:
                        ActionChains(self.driver).scroll_to_element(row_xpath).perform()
                        href_data = row_xpath.get_attribute("href")
                        row_xpath.click()
                        # print_row = self.driver.find_element(By.XPATH,"//table//tr[21]//td[1]").text
                        # print("Row Print",print_row)
                        time.sleep(2)
                        self.get_data_delete(row_xpath)
                    else:
                        print("This element already deleted..")
                except Exception as e:
                    print("This element already deleted..")
            time.sleep(3)
        except Exception as e:
            print(f"Error : {e}")


    def get_data_delete(self,data):
        try:
            # update_msg_text = self.driver.find_element(By.XPATH,"//h4[1]")
            data_display = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h4[1]")))
            if data_display.is_displayed():
                ActionChains(self.driver).scroll_to_element(data_display).perform()
                print(data_display.text)
            else:
                print("Element is not displayed.")
        except Exception as e:
            print(f"Error : This element Already deleted... if you want delete the please enter the another data in the code..")
        finally:
            back_to_home = self.driver.find_element(By.XPATH,"//button[@class='btn1']")
            ActionChains(self.driver).move_to_element(back_to_home).perform()
            time.sleep(3)
            back_to_home.click()
            time.sleep(3)

    # close browser
    def close_browser(self):
        self.driver.quit()
my_obj = AppTest()
my_obj.element_access()
my_obj.product_add()
my_obj.get_product_to_update()
my_obj.product_delete()
my_obj.close_browser()