import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException


def extract_job_data(job_element, seen_job_ids):
    """리스트 페이지에서 공고 데이터를 추출."""
    try:
        input_values = job_element.find_element(By.CSS_SELECTOR, 'input').get_attribute('value').split('|')
        job_id = input_values[0]

        if job_id in seen_job_ids:
            return None

        # 요소를 다시 가져오는 방식으로 stale element reference 문제 완화
        location, salary = None, None
        max_retries = 3
        for _ in range(max_retries):
            try:
                location = job_element.find_element(By.CSS_SELECTOR, '.site').text
                salary = job_element.find_element(By.CSS_SELECTOR, '.b1_sb').text
                break
            except StaleElementReferenceException:
                print("Retrying stale element...")
                continue

        if not location or not salary:
            raise StaleElementReferenceException("Failed to fetch elements after retries")

        return {
            "title": input_values[3],
            "company_name": input_values[2],
            "location": location,
            "salary": salary,
            "job_id": job_id,
            "url": f"https://www.work.go.kr/empInfo/empInfoSrch/detail/empDetailAuthView.do?wantedAuthNo={job_id}",
        }
    except (StaleElementReferenceException, NoSuchElementException) as error:
        print(f"Error extracting job data: {error}")
        return None


def extract_detailed_job_data(driver, job_url):
    """상세 페이지 데이터를 추출."""
    try:
        driver.get(job_url)

        # 채용 제목 가져오기
        # title_element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "p.tit"))
        # )
        # job_title = title_element.text

        # 모집 직종 가져오기
        job_overview_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".careers-table"))
        )
        job_overview = job_overview_element.text

        # .careers-table.center 클래스가 적용된 모든 요소 가져오기
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".careers-table.center"))
        )

        table_data = []
        for table in elements:
            headers = [th.text.strip() for th in table.find_elements(By.CSS_SELECTOR, "thead th")]
            rows = []
            for row in table.find_elements(By.CSS_SELECTOR, "tbody tr"):
                cells = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
                rows.append(cells)

            formatted_table = {header: [] for header in headers}
            for row in rows:
                for index, cell in enumerate(row):
                    if index < len(headers):
                        formatted_table[headers[index]].append(cell)
            table_data.append(formatted_table)

        return {
            "job_overview": job_overview,
            "details": table_data,
        }
    except TimeoutException:
        print(f"Timeout while loading detailed job data from {job_url}")
        return None
    except Exception as e:
        print(f"Error extracting detailed job data from {job_url}: {e}")
        return None


def format_job_data(job_data, index):
    """채용공고 데이터를 보기 좋게 포맷팅"""
    formatted_data = {
        "공고번호": index + 1,  # 1부터 시작하는 순번
        "채용제목": job_data["title"],
        "회사명": job_data["company_name"],
        "근무지역": job_data["location"],
        "급여조건": job_data["salary"],
        "채용공고ID": job_data["job_id"],
        "채용공고URL": job_data["url"],
        "상세정보": {
            "직무내용": job_data.get("job_overview", ""),
            "세부요건": job_data.get("details", [])
        }
    }
    return formatted_data


def crawl_jobs_with_details(search_query, output_file="jobs_with_details.json"):
    """공고 목록과 상세 정보를 크롤링."""
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()

    collected_jobs = []
    seen_job_ids = set()
    current_page = 1
    previous_page_job_ids = []

    try:
        while True:
            # 목록 페이지 URL
            list_url = f"https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do?srcKeyword={search_query}&pageIndex={current_page}"
            driver.get(list_url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#contentArea'))
            )

            # 현재 페이지의 모든 공고 요소 가져오기
            job_elements = driver.find_elements(By.CSS_SELECTOR, '#contentArea > tbody > tr')
            current_page_job_ids = []
            page_jobs = []  # 현재 페이지의 공고 데이터 임시 저장

            # 현재 페이지의 기본 데이터 먼저 수집
            for job_element in job_elements:
                job_data = extract_job_data(job_element, seen_job_ids)
                if job_data:
                    page_jobs.append(job_data)
                    current_page_job_ids.append(job_data["job_id"])

            # 수집된 기본 데이터에 대해 상세 정보 수집
            for job_data in page_jobs:
                try:
                    # 상세 페이지 조회
                    detailed_data = extract_detailed_job_data(driver, job_data["url"])
                    if detailed_data:
                        job_data.update(detailed_data)
                    
                    # 중복 방지를 위한 처리
                    if job_data["job_id"] not in seen_job_ids:
                        collected_jobs.append(job_data)
                        seen_job_ids.add(job_data["job_id"])
                    
                    # 목록 페이지로 돌아가기
                    driver.get(list_url)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '#contentArea'))
                    )
                except Exception as e:
                    print(f"상세 페이지 처리 중 오류 발생: {e}")
                    continue

            print(f"현재 페이지({current_page}) 수집된 공고 수: {len(current_page_job_ids)}")

            if set(current_page_job_ids) == set(previous_page_job_ids):
                print(f"마지막 페이지 도달: {current_page}페이지")
                break

            if not current_page_job_ids:
                print(f"데이터가 없는 페이지 도달: {current_page}페이지")
                break

            previous_page_job_ids = current_page_job_ids
            current_page += 1

        print(f"총 수집된 채용공고 수: {len(collected_jobs)}")

        # 수집된 데이터 포맷팅
        formatted_jobs = {
            "검색조건": search_query,
            "총_채용공고수": len(collected_jobs),
            "수집일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "채용공고목록": [format_job_data(job, idx) for idx, job in enumerate(collected_jobs)]
        }

        # JSON 파일 저장
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(formatted_jobs, file, ensure_ascii=False, indent=2)

        return formatted_jobs

    finally:
        driver.quit()


if __name__ == "__main__":
    crawl_jobs_with_details("고령자", "jobs_with_details.json")
