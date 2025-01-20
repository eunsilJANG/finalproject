import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def crawl_jobs(search_query, output_file="indeed.json"):
    """검색어를 기반으로 Indeed 채용공고를 크롤링합니다."""

    # 크롬 드라이버를 자동으로 설치하거나 이미 설치된 버전을 사용합니다.
    chromedriver_autoinstaller.install()

    # Selenium을 사용해 크롬 브라우저를 실행합니다.
    driver = webdriver.Chrome()

    # 수집된 채용 공고 데이터를 저장할 리스트
    collected_jobs = []

    # 이미 처리한 채용 공고 ID를 저장하는 집합(Set)
    seen_job_ids = set()

    # 현재 페이지 번호를 나타내며, 시작값은 0
    current_page = 0

    # 이전 페이지에서 수집한 채용 공고 ID 리스트
    previous_page_job_ids = []

    try:
        while True:
            # 검색어와 페이지 번호를 기반으로 검색 결과 페이지 URL 생성
            # Indeed에서 검색 결과는 한 페이지에 10개의 공고가 표시. 페이지가 넘어갈수록 공고의 **시작 위치(index)**가 10씩 증가
            url = f"https://kr.indeed.com/jobs?q={search_query}&start={current_page * 10}"
            
            # 해당 페이지를 브라우저에서 로드
            driver.get(url)

            # 검색 결과의 주요 요소(채용 공고 카드)가 로드될 때까지 최대 10초 대기
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.css-1ac2h1w.eu4oa1w0'))
            )

            # 현재 페이지에 있는 모든 채용 공고 요소를 리스트로 저장
            job_elements = driver.find_elements(By.CSS_SELECTOR, '.css-1ac2h1w.eu4oa1w0')

            # 현재 페이지에서 추출한 공고 ID를 저장할 리스트
            current_page_job_ids = []

            # 각 채용 공고 요소를 순회하며 데이터 처리
            for job_element in job_elements:
                # 공고 데이터를 추출하고 중복 방지
                job_details = extract_job_details(job_element, seen_job_ids)

                if job_details:
                    # 유효한 공고 데이터를 수집 리스트에 추가
                    collected_jobs.append(job_details)

                    # 해당 공고의 ID를 현재 페이지 ID 리스트에 저장
                    current_page_job_ids.append(job_details["job_id"])

            # 이전 페이지와 현재 페이지의 공고 ID가 동일하면 마지막 페이지로 간주하고 종료
            if set(current_page_job_ids) == set(previous_page_job_ids):
                print(f"마지막 페이지 도달: {current_page}페이지")
                break

            # 현재 페이지에서 공고 ID가 없으면 크롤링 종료
            if not current_page_job_ids:
                print(f"데이터가 없는 페이지 도달: {current_page}페이지")
                break

            # 이전 페이지의 공고 ID를 업데이트
            previous_page_job_ids = current_page_job_ids

            # 페이지 번호를 증가시켜 다음 페이지로 이동
            current_page += 1

        # 총 수집된 채용 공고 수를 출력
        print(f"총 수집된 채용공고 수: {len(collected_jobs)}")
    finally:
        # 크롬 드라이버를 종료하여 시스템 리소스를 해제
        driver.quit()

    # 수집된 데이터를 JSON 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(collected_jobs, file, ensure_ascii=False, indent=2)

    # 크롤링된 데이터를 리스트 형태로 반환
    return collected_jobs

def extract_job_details(job_element, seen_job_ids):
    """채용 공고 데이터를 추출하는 함수."""
    try:
        # 채용 공고 링크를 가진 <a> 태그에서 고유한 ID 추출
        job_link_element = job_element.find_element(By.CSS_SELECTOR, 'a[data-jk]')
        job_id = job_link_element.get_attribute('data-jk')

        # 이미 처리된 공고 ID라면 중복 방지
        if job_id in seen_job_ids:
            return None
        seen_job_ids.add(job_id)

        # 회사명과 위치 정보를 포함한 요소
        location_element = job_element.find_element(By.CSS_SELECTOR, '.company_location.css-i375s1.e37uo190')

        # 공고 데이터를 딕셔너리 형태로 반환
        return {
            "title": job_link_element.find_element(By.CSS_SELECTOR, 'span').get_attribute('title'),
            "company_name": location_element.find_element(By.CSS_SELECTOR, '.css-1h7lukg.eu4oa1w0').text,
            "location": location_element.find_element(By.CSS_SELECTOR, '.css-1restlb.eu4oa1w0').text,
            "salary": extract_salary(job_element),
            "job_id": job_id,
            "url": f"https://kr.indeed.com/viewjob?jk={job_id}",
        }
    except Exception as error:
        # 데이터가 없거나 오류 발생 시 None 반환
        print(f"Error extracting job details: {error}")
        return None

def extract_salary(job_element):
    """급여 정보를 추출하는 함수."""
    try:
        # 급여 정보를 포함한 HTML 요소 추출
        salary_element = job_element.find_element(By.CSS_SELECTOR, '.css-18z4q2i.eu4oa1w0')
        return salary_element.text if salary_element.text else "-"
    except Exception:
        # 급여 정보가 없으면 기본값 반환
        return "-"

if __name__ == "__main__":
    # "고령자"를 검색어로 크롤링을 수행하며, 결과를 "indeed.json" 파일로 저장
    crawl_jobs("고령자", "indeed.json")
