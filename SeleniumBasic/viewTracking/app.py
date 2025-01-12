import time
from selenium import webdriver
from selenium.webdriver.common.by import By

import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()

검색쿼리="python flask"
search_link = f"https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query={검색쿼리}"
driver.get(search_link)
time.sleep(2)

target_blog_link="https://blog.naver.com/urmyver/223621480150"
링크_셀렉터 =   f'a[href^="{target_blog_link}"]'
element = driver.find_element(By.CSS_SELECTOR, 링크_셀렉터)

input()