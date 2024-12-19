from requests import options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

Options = ChromeOptions()

# 브라우저가 요청을 보내면 아래의 user_agent를 보내게 되어 있다.
# 이걸 안주면 차단 당할 수 있다.
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'

Options.add_argument('user_agent=' + user_agent)
Options.add_argument('long=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=Options)

url = 'https://news.naver.com/section/100'
driver.get(url)
button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'

for i in range(15):
    time.sleep(0.5)
    driver.find_element(By.XPATH, button_xpath).click()

time.sleep(30)

driver.close()

