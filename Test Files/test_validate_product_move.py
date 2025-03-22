from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from excel_utils_functions import write_data, read_data, row_count
import allure
import openpyxl
import time
import pytest
import logging

class TestProductValidate:
    def setup_class(self):
        self.file_path = "E:\PythonWebAPP-PythonWebApp_Dev_old\PythonWebAPP-PythonWebApp_Dev\Inventory_Test_Data.xlsx"

    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_delete_check_movement(self):
        row_counts = row_count(self.file_path, "Product Movement Data")
        print("Row Counts",row_counts)
        for row in range(2, row_counts+1):
            product_id = read_data(self.file_path,"Product Movement Data", row, 1)
            print("Product ID",product_id)
            