import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_job_data(job_element, seen_job_ids):
    """채용 공고 데이터를 추출."""
    try:
        # 공고 데이터를 포함한 input 요소의 value 속성을 추출
        # value는 '|'로 구분된 문자열이며, 이를 분리하여 필요한 데이터를 가져옵니다.
        input_values = job_element.find_element(By.CSS_SELECTOR, 'input').get_attribute('value').split('|')
        job_id = input_values[0]  # 공고의 고유 ID

        # 이미 처리된 공고 ID는 중복 방지
        if job_id in seen_job_ids:
            return None

        # 공고 데이터를 딕셔너리 형태로 반환
        return {
            "title": input_values[3],  # 공고 제목
            "company": input_values[2],  # 회사 이름
            "location": job_element.find_element(By.CSS_SELECTOR, '.site').text,  # 공고 위치
            "salary": job_element.find_element(By.CSS_SELECTOR, '.b1_sb').text,  # 급여 정보
            "job_id": job_id,  # 고유 ID
            "link": f"https://www.work.go.kr/empInfo/empInfoSrch/detail/empDetailAuthView.do?wantedAuthNo={job_id}",  # 상세 공고 링크
        }
    except Exception as error:
        # 오류 발생 시 로그 출력
        print(f"Error extracting job data: {error}")
        return None

def crawl_jobs(search_query, output_file="jobs.json"):
    """검색어를 기반으로 채용공고를 크롤링"""

    # 크롬 드라이버 설치 및 초기화
    # chromedriver_autoinstaller는 크롬 버전에 맞는 드라이버를 자동으로 설치합니다.
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()

    # 수집된 공고 데이터와 중복 방지용 ID 집합 초기화
    collected_jobs = []  # 최종적으로 수집된 공고 데이터를 저장
    seen_job_ids = set()  # 이미 처리한 공고 ID를 저장해 중복을 방지
    current_page = 1  # 시작 페이지 번호
    previous_page_job_ids = []  # 이전 페이지의 공고 ID를 저장

    try:
        while True:
            # 검색어와 페이지 번호를 기반으로 URL 생성
            # 페이지 번호는 pageIndex 파라미터로 전달됩니다.
            url = f"https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do?srcKeyword={search_query}&pageIndex={current_page}"
            driver.get(url)  # 해당 URL로 브라우저 이동

            # 페이지 로드 대기
            # '#contentArea' 요소가 나타날 때까지 최대 10초 대기
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#contentArea'))
            )

            # 채용 공고 요소 추출
            # '#contentArea > tbody > tr'는 공고 리스트를 나타냅니다.
            job_elements = driver.find_elements(By.CSS_SELECTOR, '#contentArea > tbody > tr')
            current_page_job_ids = []  # 현재 페이지에서 처리된 공고 ID를 저장

            # 각 공고 데이터 처리
            for job_element in job_elements:
                # 공고 데이터를 추출하고 중복 방지
                job_data = extract_job_data(job_element, seen_job_ids)
                if job_data:
                    collected_jobs.append(job_data)  # 유효한 공고 데이터를 수집 리스트에 추가
                    current_page_job_ids.append(job_data["job_id"])  # 해당 공고 ID를 현재 페이지 리스트에 저장

            # 이전 페이지와 현재 페이지의 공고 ID가 동일하면 종료
            if set(current_page_job_ids) == set(previous_page_job_ids):
                print(f"마지막 페이지 도달: {current_page}페이지")
                break

            # 공고 데이터가 없으면 종료
            if not current_page_job_ids:
                print(f"데이터가 없는 페이지 도달: {current_page}페이지")
                break

            # 다음 페이지 준비
            previous_page_job_ids = current_page_job_ids
            current_page += 1  # 페이지 번호 증가

        # 총 수집된 공고 수 출력
        print(f"총 수집된 채용공고 수: {len(collected_jobs)}")

    finally:
        # 드라이버 종료
        driver.quit()

    # 결과를 JSON 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(collected_jobs, file, ensure_ascii=False, indent=2)

    # 수집된 공고 데이터 반환
    return collected_jobs

if __name__ == "__main__":
    # "고령자" 검색어로 크롤링 수행
    # 결과는 'work24.json' 파일로 저장됩니다.
    crawl_jobs("고령자", "work24.json")
