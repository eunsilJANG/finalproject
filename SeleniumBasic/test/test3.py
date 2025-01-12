import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import chromedriver_autoinstaller

# ChromeDriver 자동 설치
chromedriver_autoinstaller.install()

driver = webdriver.Chrome()

# 1. 타겟 URL 열기
url = "https://kr.indeed.com/q-%EA%B3%A0%EB%A0%B9%EC%9E%90-%EC%B1%84%EC%9A%A9%EA%B3%A0.html"
driver.get(url)
time.sleep(3)  # 페이지 로딩 대기

# 2. 데이터 추출
job_cards = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')  # 공고 전체를 감싸는 클래스

data = []
for job in job_cards:
    # 공고 제목
    try:
        title = job.find_element(By.CLASS_NAME, 'jcs-JobTitle').text.strip()
    except:
        title = "제목 없음"

    # 링크
    try:
        link = job.find_element(By.CLASS_NAME, 'jcs-JobTitle').get_attribute('href')
    except:
        link = "링크 없음"

    # 회사 이름과 위치를 링크에서 가져오기
    companyname = "정보 없음"
    location = "정보 없음"
    if link != "링크 없음":
        try:
            driver.execute_script("window.open(arguments[0]);", link)  # 새 탭 열기
            driver.switch_to.window(driver.window_handles[-1])  # 새 탭으로 전환
            time.sleep(3)  # 페이지 로딩 대기

            # 회사 이름과 위치 추출 (id나 class는 공고 페이지에 따라 변경 필요)
            try:
                companyname = driver.find_element(By.ID, 'company-name-id').text.strip()  # 회사 이름 id 확인
            except:
                companyname = "정보 없음"

            try:
                location = driver.find_element(By.ID, 'location-id').text.strip()  # 위치 id 확인
            except:
                location = "정보 없음"
            
            driver.close()  # 탭 닫기
            driver.switch_to.window(driver.window_handles[0])  # 원래 탭으로 전환
        except Exception as e:
            print(f"링크 처리 중 오류 발생: {e}")

    print(f"공고 제목: {title}")
    print(f"회사 이름: {companyname}")
    print(f"회사 위치: {location}")
    print(f"공고 링크: {link}")
    print("-" * 50)
    
    data.append({
        "title": title,
        "company": companyname,
        "location": location,
        "link": link,
    })

# JSON 파일로 저장
with open('jobs.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("크롤링 데이터를 jobs.json 파일에 저장했습니다.")
driver.quit()
