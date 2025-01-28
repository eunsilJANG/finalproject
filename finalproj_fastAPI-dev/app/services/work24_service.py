from typing import Dict, List, Optional, Any
import httpx
import xmltodict
import json
from datetime import datetime
from ..core.config import settings

class Work24Service:
    def __init__(self):
        self.api_key = settings.WORK24_API_KEY
        self.base_url = settings.WORK24_API_BASE_URL

    async def fetch_job_postings(
        self,
        start_page: int = 1,
        display: int = 100,  # 최대 100개
        region: Optional[str] = None,
        job_type: Optional[str] = None,
        age_target: Optional[str] = None,
        keyword: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """채용정보 목록 조회"""
        try:
            # 채용정보 목록 API 엔드포인트
            url = f"{self.base_url}/callOpenApiSvcInfo210L01.do"
            
            # API 요청 파라미터
            params = {
                "authKey": self.api_key,
                "returnType": "XML",
                "startPage": start_page,
                "display": display,
                "region": region,
                "occupation": job_type,
                # "empTpGb": "2",  # 임용직
                "pfPreferential": "B",  # (주)고령자(50세이상)
                "sortOrderBy": "DESC",  # 등록일 상향정렬
                "maxWantedAuthDt": None,  # 최대 구인인증일자
                "comPreferential": None,  # 우대조건 (기업)
                "major": None,  # 전공코드
                "foreignLanguage": None,  # 외국어코드
                "keyword": keyword
            }
            
            # None 값 제거
            params = {k: v for k, v in params.items() if v is not None}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                # XML 응답을 파싱
                data = xmltodict.parse(response.text)
                jobs = data.get("jobs", {}).get("job", [])
                
                if not isinstance(jobs, list):
                    jobs = [jobs] if jobs else []
                
                return jobs

        except Exception as e:
            print(f"채용정보 조회 중 오류 발생: {str(e)}")
            return []

    async def fetch_job_detail(self, job_id: str) -> Optional[Dict[str, Any]]:
        """채용정보 상세 조회"""
        try:
            # 채용정보 상세 API 엔드포인트
            url = f"{self.base_url}/callOpenApiSvcInfo210D01.do"
            
            params = {
                "authKey": self.api_key,
                "returnType": "XML",
                "wantedAuthNo": job_id  # 채용공고 번호
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                # XML 응답을 파싱
                data = xmltodict.parse(response.text)
                job_detail = data.get("job", {})
                
                return job_detail if job_detail else None

        except Exception as e:
            print(f"채용상세정보 조회 중 오류 발생: {str(e)}")
            return None

    def _convert_emp_type(self, emp_type_code: str) -> str:
        """고용형태 코드를 문자열로 변환"""
        emp_type_map = {
            "10": "정규직",
            "11": "정규직(시간선택제)",
            "20": "계약직",
            "21": "계약직(시간선택제)",
            "4": "파견직",
            "Y": "대체인력"
        }
        return emp_type_map.get(emp_type_code, "기타")

    async def fetch_codes(self, code_type: str) -> List[Dict[str, str]]:
        try:
            params = {
                "authKey": self.api_key,
                "returnType": "XML",
                "target": "CMCD",
                "dtlGb": "1"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/callOpenApiSvcInfo21L01.do", params=params)
                response.raise_for_status()
                
                data = xmltodict.parse(response.text)
                print(f"XML 응답: {data}")  # 디버그 로그 추가
                
                codes = []
                if code_type == "region":
                    root = data.get("cmcdRegion", {})
                    one_depth_items = root.get("oneDepth", [])
                    if not isinstance(one_depth_items, list):
                        one_depth_items = [one_depth_items]
                    
                    for item in one_depth_items:
                        code = {
                            "code": item.get("regionCd", ""),
                            "name": item.get("regionNm", ""),
                            "sub_codes": []
                        }
                        
                        two_depth_items = item.get("twoDepth", [])
                        if not isinstance(two_depth_items, list):
                            two_depth_items = [two_depth_items]
                        
                        for sub_item in two_depth_items:
                            sub_code = {
                                "code": sub_item.get("regionCd", ""),
                                "name": sub_item.get("regionNm", ""),
                                "super_code": sub_item.get("superCd", "")
                            }
                            code["sub_codes"].append(sub_code)
                        
                        codes.append(code)
                
                print(f"파싱 결과: {codes}")  # 디버그 로그 추가
                return codes
                
        except Exception as e:
            import traceback
            print(f"오류 발생: {str(e)}")
            print(f"오류 상세: {e.__class__.__name__}")
            print(f"스택 트레이스: {traceback.format_exc()}")
            return [] 