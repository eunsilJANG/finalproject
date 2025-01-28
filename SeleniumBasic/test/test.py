import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# WebDriver 설정
driver = webdriver.Chrome()

try:
    # 페이지 로드
    driver.get("https://www.work.go.kr/empInfo/empInfoSrch/detail/empDetailAuthView.do?wantedAuthNo=KC5I492501170003#1")

    # 채용 제목 가져오기
    title_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "p.tit"))
    )
    job_title = title_element.text

    # 모집 직종 가져오기
    job_category_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".careers-new"))
    )
    job_category = job_category_element.text

    # .careers-table.center 클래스가 적용된 모든 요소 가져오기
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".careers-table.center"))
    )

    # 각 요소의 텍스트를 리스트에 저장
    table_data = []
    for index, element in enumerate(elements, start=1):
        table_data.append({
            "index": index,
            "content": element.text
        })

    # 데이터를 JSON 형식으로 저장
    job_data = {
        "job_title": job_title,
        "job_category": job_category,
        "table_data": table_data
    }

    # JSON 파일 저장
    with open("job_data.json", "w", encoding="utf-8") as json_file:
        json.dump(job_data, json_file, ensure_ascii=False, indent=4)

    print("데이터가 JSON 파일로 저장되었습니다: job_data.json")

except Exception as e:
    print(f"에러 발생: {e}")

finally:
    driver.quit()
