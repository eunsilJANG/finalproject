import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_work24_job_data(job_element, seen_job_ids):
    """Work24 채용 공고 데이터를 추출."""
    try:
        # 공고 데이터를 포함한 input 요소 확인 및 추출
        input_element = job_element.find_elements(By.CSS_SELECTOR, 'input')
        if not input_element:
            print("Input element not found, skipping this job.")
            return None

        # value 속성을 가져와 공고 데이터를 분리
        input_values = input_element[0].get_attribute('value').split('|')
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
            "source": "Work24"  # 데이터 출처 정보 추가
        }
    except Exception as error:
        # 오류 발생 시 로그 출력
        print(f"Error extracting Work24 job data: {error}")
        return None

def extract_indeed_job_data(job_element, seen_job_ids):
    """Indeed 채용 공고 데이터를 추출."""
    try:
        # 채용 공고 링크를 가진 <a> 태그에서 고유한 ID 추출
        job_link_element = job_element.find_element(By.CSS_SELECTOR, 'a[data-jk]')
        job_id = job_link_element.get_attribute('data-jk')

        # 이미 처리된 공고 ID는 중복 방지
        if job_id in seen_job_ids:
            return None
        seen_job_ids.add(job_id)

        # 회사명과 위치 정보를 포함한 요소
        location_element = job_element.find_element(By.CSS_SELECTOR, '.company_location.css-i375s1.e37uo190')

        # 공고 데이터를 딕셔너리 형태로 반환
        return {
            "title": job_link_element.find_element(By.CSS_SELECTOR, 'span').get_attribute('title'),  # 공고 제목
            "company": location_element.find_element(By.CSS_SELECTOR, '.css-1h7lukg.eu4oa1w0').text,  # 회사 이름
            "location": location_element.find_element(By.CSS_SELECTOR, '.css-1restlb.eu4oa1w0').text,  # 공고 위치
            "salary": extract_indeed_salary(job_element),  # 급여 정보
            "job_id": job_id,  # 고유 ID
            "link": f"https://kr.indeed.com/viewjob?jk={job_id}",  # 상세 공고 링크
            "source": "Indeed"  # 데이터 출처 정보 추가
        }
    except Exception as error:
        # 오류 발생 시 로그 출력
        print(f"Error extracting Indeed job data: {error}")
        return None

def extract_indeed_salary(job_element):
    """Indeed 급여 정보를 추출."""
    try:
        # 급여 정보를 포함한 HTML 요소 추출
        salary_element = job_element.find_element(By.CSS_SELECTOR, '.css-18z4q2i.eu4oa1w0')
        return salary_element.text if salary_element.text else "-"
    except Exception:
        # 급여 정보가 없으면 기본값 반환
        return "-"

def crawl_work24_jobs(search_query):
    """Work24 채용 공고 크롤링."""
    # 크롬 드라이버 자동 설치 및 초기화
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    collected_jobs = []  # 수집된 공고 데이터를 저장
    seen_job_ids = set()  # 중복 방지용 ID 집합
    current_page = 1  # 시작 페이지 번호

    try:
        while True:
            # 검색어와 페이지 번호를 기반으로 URL 생성
            url = f"https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do?srcKeyword={search_query}&pageIndex={current_page}"
            driver.get(url)

            # 페이지 로드 대기
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#contentArea'))
            )

            # 채용 공고 요소 추출
            job_elements = driver.find_elements(By.CSS_SELECTOR, '#contentArea > tbody > tr')

            for job_element in job_elements:
                job_data = extract_work24_job_data(job_element, seen_job_ids)
                if job_data:
                    collected_jobs.append(job_data)  # 유효한 공고 데이터 저장

            # 공고 요소가 없으면 종료
            if not job_elements:
                break

            # 다음 페이지로 이동
            current_page += 1

    finally:
        # 드라이버 종료
        driver.quit()

    return collected_jobs

def crawl_indeed_jobs(search_query):
    """Indeed 채용 공고 크롤링."""
    # 크롬 드라이버 자동 설치 및 초기화
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    collected_jobs = []  # 수집된 공고 데이터를 저장
    seen_job_ids = set()  # 중복 방지용 ID 집합
    current_page = 0  # 시작 페이지 번호

    try:
        while True:
            # 검색어와 페이지 번호를 기반으로 URL 생성
            url = f"https://kr.indeed.com/jobs?q={search_query}&start={current_page * 10}"
            driver.get(url)

            # 페이지 로드 대기
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.css-1ac2h1w.eu4oa1w0'))
            )

            # 채용 공고 요소 추출
            job_elements = driver.find_elements(By.CSS_SELECTOR, '.css-1ac2h1w.eu4oa1w0')

            for job_element in job_elements:
                job_data = extract_indeed_job_data(job_element, seen_job_ids)
                if job_data:
                    collected_jobs.append(job_data)  # 유효한 공고 데이터 저장

            # 공고 요소가 없으면 종료
            if not job_elements:
                break

            # 다음 페이지로 이동
            current_page += 1

    finally:
        # 드라이버 종료
        driver.quit()

    return collected_jobs

def merge_and_save_jobs(search_query, output_file="jobs.json"):
    """Work24와 Indeed에서 데이터를 크롤링하고 병합하여 저장."""
    print("Work24 크롤링 시작...")
    work24_jobs = crawl_work24_jobs(search_query)
    print(f"Work24 크롤링 완료: {len(work24_jobs)}건 수집")

    print("Indeed 크롤링 시작...")
    indeed_jobs = crawl_indeed_jobs(search_query)
    print(f"Indeed 크롤링 완료: {len(indeed_jobs)}건 수집")

    # 두 사이트의 데이터를 병합
    merged_jobs = work24_jobs + indeed_jobs

    # 병합된 데이터를 JSON 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(merged_jobs, file, ensure_ascii=False, indent=2)

    print(f"총 {len(merged_jobs)}건의 데이터가 {output_file}에 저장되었습니다.")

if __name__ == "__main__":
    # "고령자" 검색어로 데이터를 병합하여 저장
    merge_and_save_jobs("고령자", "jobs.json")
