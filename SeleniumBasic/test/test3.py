import json
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
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.tit"))
        )
        job_title = title_element.text

        # 모집 직종 가져오기
        job_category_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".careers-table"))
        )
        job_category = job_category_element.text

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
            "job_title": job_title,
            "job_category": job_category,
            "details": table_data,
        }
    except TimeoutException:
        print(f"Timeout while loading detailed job data from {job_url}")
        return None
    except Exception as e:
        print(f"Error extracting detailed job data from {job_url}: {e}")
        return None


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
            url = f"https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do?srcKeyword={search_query}&pageIndex={current_page}"
            driver.get(url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#contentArea'))
            )

            job_elements = driver.find_elements(By.CSS_SELECTOR, '#contentArea tbody tr')
            current_page_job_ids = []

            for job_element in job_elements:
                job_data = extract_job_data(job_element, seen_job_ids)
                if job_data:
                    # 상세페이지 데이터 수집
                    detailed_data = extract_detailed_job_data(driver, job_data["url"])
                    if detailed_data:
                        job_data.update(detailed_data)
                    collected_jobs.append(job_data)
                    seen_job_ids.add(job_data["job_id"])
                    current_page_job_ids.append(job_data["job_id"])

            if set(current_page_job_ids) == set(previous_page_job_ids):
                print(f"마지막 페이지 도달: {current_page}페이지")
                break

            if not current_page_job_ids:
                print(f"데이터가 없는 페이지 도달: {current_page}페이지")
                break

            previous_page_job_ids = current_page_job_ids
            current_page += 1

        print(f"총 수집된 채용공고 수: {len(collected_jobs)}")

    finally:
        driver.quit()

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(collected_jobs, file, ensure_ascii=False, indent=2)

    return collected_jobs


if __name__ == "__main__":
    crawl_jobs_with_details("고령자", "jobs_with_details.json")
