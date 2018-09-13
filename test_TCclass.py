#-*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars")

options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,     # 1:allow, 2:block
    "profile.default_content_setting_values.media_stream_camera": 1,  # 1:allow, 2:block
    "profile.default_content_setting_values.geolocation": 1,          # 1:allow, 2:block
    "profile.default_content_setting_values.notifications": 1         # 1:allow, 2:block
  })

class testTCclass(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(30)
        self.base_url = "https://tc.aculearn.cn/command/10170876/zr4ebc"
        self.classin_url = "https://class.aculearn.cn/#/classroom"

    def test_TCclass_login(self):
        #登录上课系统-->关闭设备检测界面-->判断
        driver = self.driver
        driver.get(self.base_url)

        #上课系统登录
        driver.find_element_by_id('tc-name').send_keys('\(^o^)/~')
        driver.find_element_by_id('tc-password').send_keys('4068')
        driver.find_element_by_tag_name('button').click()

        #关闭设备检测界面
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'tcs')))
        driver.find_element_by_xpath('//*[@id="tcs"]/div/div/div[2]/div[3]/div[1]/i').click()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'beginBtn')))
        self.assertNotEqual(self.base_url, driver.current_url)

    def test_TCclass_classin(self):
        # 登录上课系统-->关闭设备检测界面-->点击上课按钮-->判断
        driver = self.driver
        driver.get(self.base_url)

        #上课系统登录
        driver.find_element_by_id('tc-name').send_keys('\(^o^)/~')
        driver.find_element_by_id('tc-password').send_keys('4068')
        driver.find_element_by_tag_name('button').click()

        #关闭设备检测界面
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'tcs')))
        driver.find_element_by_xpath('//*[@id="tcs"]/div/div/div[2]/div[3]/div[1]/i').click()

        #点击上课按钮
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'beginBtn')))
        bgBtn = driver.find_element_by_class_name('beginBtn')
        print(bgBtn.text)
        bgBtn.click()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'in-class')))
        print(bgBtn.text)
        self.assertEqual('End Class', bgBtn.text)

    def test_TCclass_YouTube(self):
        #登录上课系统-->关闭设备检测界面-->点击上课按钮-->播放YouTube视频-->判断
        driver = self.driver
        driver.get(self.base_url)

        #上课系统登录
        driver.find_element_by_id('tc-name').send_keys('\(^o^)/~')
        driver.find_element_by_id('tc-password').send_keys('4068')
        driver.find_element_by_tag_name('button').click()

        # 关闭设备检测界面
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'tcs')))
        driver.find_element_by_xpath('//*[@id="tcs"]/div/div/div[2]/div[3]/div[1]/i').click()

        # 点击上课按钮
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'beginBtn')))
        bgBtn = driver.find_element_by_class_name('beginBtn')
        bgBtn.click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'in-class')))

        # 模拟播放视频
        driver.find_elements_by_class_name('tab-item')[-1].click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'video-item')))
        driver.find_elements_by_class_name('video-item')[-1].click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'modal')))

        driver.find_element_by_xpath(
            '//*[@id="tcs"]/div/div/div[1]/section[1]/div[3]/div/div[3]/div/div/div[1]/div/input').send_keys(
            'https://www.youtube.com/watch?v=eZMH6Mo0f9A')
        driver.find_element_by_class_name('done').click()


    def test_TCclass_classoff(self ):
        #登录上课系统-->关闭设备检测界面-->点击上课按钮-->点击下课按钮-->判断
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id('tc-name').send_keys('\(^o^)/~')
        driver.find_element_by_id('tc-password').send_keys('4068')
        driver.find_element_by_tag_name('button').click()

        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.ID, 'tcs')))
        driver.find_element_by_xpath('//*[@id="tcs"]/div/div/div[2]/div[3]/div[1]/i').click()

        # 开始上课测试
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'beginBtn')))
        bgBtn = driver.find_element_by_class_name('beginBtn')
        bgBtn.click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'in-class')))

        # 结束上课测试
        time.sleep(3)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'beginBtn')))
        bgBtn = driver.find_element_by_class_name('beginBtn')
        bgBtn.click()
        time.sleep(1)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'cusLanInfo')))
        driver.find_element_by_xpath('//*[@id="tcs"]/div/div/div[1]/section[2]/div/div/input[2]').click()

        self.assertEqual(bgBtn.text, 'Start Class')

    def tearDown(self):
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()