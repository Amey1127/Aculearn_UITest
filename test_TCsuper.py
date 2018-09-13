import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

class testTCsuper(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        # self.driver.implicitly_wait(1)
        self.base_url = "http://tcadmin.aculearn.cn/login"

    def test_TCsuper_login(self):
        driver = self.driver
        driver.get(self.base_url)

        driver.find_element_by_id('super-account').send_keys('admin')
        driver.find_element_by_id('super-pwd').send_keys('123')
        driver.find_element_by_tag_name('button').click()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'el-dropdown')))
        self.assertNotEqual(self.base_url, driver.current_url)

    def test_TCsuper_logout(self):
        driver = self.driver
        driver.get(self.base_url)

        driver.find_element_by_id('super-account').send_keys('admin')
        driver.find_element_by_id('super-pwd').send_keys('123')
        driver.find_element_by_tag_name('button').click()

        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'el-dropdown')))
            driver.find_element_by_class_name('el-dropdown').click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'el-dropdown-menu__item')))
            btn = driver.find_elements_by_class_name('el-dropdown-menu__item')[1]
            retry = 3
            while retry > 0 :
                print(btn.text)
                if(btn.text == '退出'):
                    btn.click()
                    break
                time.sleep(1)
                retry = retry - 1

            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'super-account')))
            self.assertEqual(self.base_url, driver.current_url)

        except:
            self.assertEqual(None, driver.current_url)

    def tearDown(self):
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()
