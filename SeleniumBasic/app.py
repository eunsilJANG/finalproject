import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

chromedriver_autoinstaller.install() # 크롬 버전에 맞게 chromedriver 다운

driver = webdriver.Chrome()
# 1. 웹 브라우저 주소창을 컨트롤하기 driver.get 
driver.get("https://www.naver.com")
time.sleep(3)
driver.current_url

#2-1 요소를 찾아서 Copy 해옴. 실제 웹 브라우저 + 개발자 도구
엘리먼트_셀렉터 ="#newsstand > div.ContentHeaderView-module__content_header___nSgPg > div > ul"

#2-2. 찾아온 요소를 find_element로 가져오기 -> 상자(변수)에 담기
콘텐트헤더 = driver.find_element(By.CSS_SELECTOR, 엘리먼트_셀렉터)

#3-1 데이터를 가져오기3
print(콘텐트헤더.text)

#3-2 요소를 클릭하기[액션]
콘텐트헤더.click()

input()