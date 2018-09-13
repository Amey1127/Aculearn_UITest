#-*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from HTMLTestRunner import HTMLTestRunner
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

class testTCmanager(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://tc.aculearn.cn/login"

    def test_TCmanager_login(self):
        driver = self.driver
        driver.get(self.base_url)

        driver.find_element_by_id('tuition-domain').send_keys('AmeyTest')
        driver.find_element_by_id('tuition-account').send_keys('admin')
        driver.find_element_by_id('tuition-password').send_keys('admin')
        driver.find_element_by_tag_name('button').click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'el-dropdown-link')))
        self.assertNotEqual(self.base_url, driver.current_url)

    def test_TCmanager_logout(self):
        driver = self.driver
        driver.get(self.base_url)

        driver.find_element_by_id('tuition-domain').send_keys('AmeyTest')
        driver.find_element_by_id('tuition-account').send_keys('admin')
        driver.find_element_by_id('tuition-password').send_keys('admin')
        driver.find_element_by_tag_name('button').click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'el-dropdown-link')))

        try:
            driver.find_element_by_class_name('el-dropdown-link').click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'el-dropdown-menu__item')))
            driver.find_elements_by_class_name('el-dropdown-menu__item')[1].click()

            time.sleep(1)
            self.assertEqual('Tuition Cloud', driver.title)
        except:
            self.assertEqual( None, driver.current_url)

    def tearDown(self):
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()
