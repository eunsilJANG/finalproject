from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import chromedriver_autoinstaller

# ChromeDriver 자동 설치
chromedriver_autoinstaller.install()

driver = webdriver.Chrome()

# 1. 타겟 URL 열기
url = "https://kr.indeed.com/q-%EA%B3%A0%EB%A0%B9%EC%9E%90-%EC%B1%84%EC%9A%A9%EA%B3%B5%EA%B3%A0.html"
driver.get(url)
time.sleep(3)  # 페이지 로딩 대기

# 2. 데이터 추출
job_cards = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')  # 공고 전체를 감싸는 클래스

for job in job_cards:
    # 공고 제목
    try:
        title = job.find_element(By.CLASS_NAME, 'jcs-JobTitle').text.strip()
    except:
        title = "제목 없음"

    # 회사이름 &위치
    try:
        location = job.find_element(By.CLASS_NAME, 'company_location').text.strip()
    except:
        location = "위치 없음"

    # 링크
    try:
        link = job.find_element(By.CLASS_NAME, 'jcs-JobTitle').get_attribute('href')
    except:
        link = "링크 없음"

    print(f"공고 제목: {title}")
    print(f"회사 이름 & 위치: {location}")
    print(f"공고 링크: {link}")
    print("-" * 50)

# 3. 브라우저 종료
driver.quit()