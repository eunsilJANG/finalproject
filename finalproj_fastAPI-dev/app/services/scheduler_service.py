from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from typing import Optional
from ..core.config import settings
from .work24_service import Work24Service
from .hrd_service import HRDService
from .vector_db_service import VectorDBService
from .llm_service import LLMService
from .code_service import CodeService
import asyncio

class SchedulerService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.work24_service = Work24Service()
        self.hrd_service = HRDService()
        self.vector_db = VectorDBService()
        self.llm_service = LLMService(model_name="llama2")  # 임베딩용
        self.code_service = CodeService()  # CodeService 인스턴스 추가
        
        # 작업 상태 추적
        self.last_job_collection: Optional[datetime] = None
        self.last_training_collection: Optional[datetime] = None
        self.last_code_collection: Optional[datetime] = None  # 코드 수집 시간 추가
        self.collection_status = {
            "jobs": {"status": "idle", "count": 0, "error": None},
            "training": {"status": "idle", "count": 0, "error": None},
            "codes": {"status": "idle", "count": 0, "error": None}  # 코드 상태 추가
        }

    async def collect_jobs(self):
        """채용 정보 수집 작업"""
        try:
            self.collection_status["jobs"]["status"] = "running"
            total_count = 0
            
            # 여러 페이지의 데이터 수집
            for page in range(1, 11):  # 최대 10페이지
                # 채용정보 목록 조회
                job_postings = await self.work24_service.fetch_job_postings(
                    start_page=page,
                    display=100,  # 한 페이지당 최대 100개
                    age_target="senior",  # 고령자 일자리 필터
                    region=None,  # 전국
                    job_type=None  # 모든 직종
                )
                
                if not job_postings:
                    break
                
                for job in job_postings:
                    try:
                        # 채용상세정보 조회
                        job_detail = await self.work24_service.fetch_job_detail(
                            job_id=job.get("wantedAuthNo")
                        )
                        
                        if job_detail:
                            # 목록정보와 상세정보 병합
                            job.update(job_detail)
                        
                        # 임베딩 생성을 위한 텍스트 구성
                        job_text = f"""
                        제목: {job.get('title', '')}
                        회사: {job.get('company_name', '')}
                        위치: {job.get('location', '')}
                        직무 설명: {job.get('description', '')}
                        자격 요건: {job.get('requirements', '')}
                        근무조건: {job.get('working_conditions', '')}
                        복리후생: {job.get('benefits', '')}
                        우대사항: {job.get('preferences', '')}
                        """
                        
                        vector = await self.llm_service.embeddings.aembed_query(job_text)
                        
                        # 벡터 DB에 저장
                        success = await self.vector_db.upsert_job_posting(
                            job_posting=job,
                            vector=vector
                        )
                        
                        if success:
                            total_count += 1
                            print(f"채용공고 저장 성공: {job.get('title')}")
                            
                    except Exception as e:
                        print(f"채용 공고 처리 중 오류 발생: {str(e)}")
                        continue
            
            self.collection_status["jobs"]["status"] = "completed"
            self.collection_status["jobs"]["count"] = total_count
            self.collection_status["jobs"]["error"] = None
            self.last_job_collection = datetime.now()
            
        except Exception as e:
            self.collection_status["jobs"]["status"] = "error"
            self.collection_status["jobs"]["error"] = str(e)
            print(f"채용 정보 수집 중 오류 발생: {str(e)}")

    async def collect_training_programs(self):
        """훈련 프로그램 수집 작업"""
        try:
            self.collection_status["training"]["status"] = "running"
            total_count = 0
            
            # 여러 페이지의 데이터 수집
            for page in range(1, 11):  # 최대 10페이지
                programs = await self.hrd_service.fetch_training_programs(
                    start_page=page,
                    display=100
                )
                
                if not programs:
                    break
                
                for program in programs:
                    try:
                        # 임베딩 생성
                        program_text = f"""
                        프로그램: {program['title']}
                        기관: {program['institution']}
                        설명: {program['description']}
                        자격 요건: {program['requirements']}
                        지원금: {program['support_info']}
                        """
                        vector = await self.llm_service.embeddings.aembed_query(program_text)
                        
                        # 벡터 DB에 저장
                        success = await self.vector_db.upsert_training_program(
                            program=program,
                            vector=vector
                        )
                        
                        if success:
                            total_count += 1
                            
                    except Exception as e:
                        print(f"훈련 프로그램 처리 중 오류 발생: {str(e)}")
                        continue
            
            self.collection_status["training"]["status"] = "completed"
            self.collection_status["training"]["count"] = total_count
            self.collection_status["training"]["error"] = None
            self.last_training_collection = datetime.now()
            
        except Exception as e:
            self.collection_status["training"]["status"] = "error"
            self.collection_status["training"]["error"] = str(e)
            print(f"훈련 프로그램 수집 중 오류 발생: {str(e)}")

    async def collect_codes(self):
        """공통 코드 데이터 수집 작업"""
        try:
            self.collection_status["codes"]["status"] = "running"
            
            # 코드 데이터 수집
            codes = await self.code_service.get_all_codes()
            
            if codes:
                self.collection_status["codes"]["count"] = sum(len(v) for v in codes.values())
                self.collection_status["codes"]["status"] = "completed"
                self.collection_status["codes"]["error"] = None
                self.last_code_collection = datetime.now()
            
        except Exception as e:
            self.collection_status["codes"]["status"] = "error"
            self.collection_status["codes"]["error"] = str(e)
            print(f"코드 데이터 수집 중 오류 발생: {str(e)}")

    def start(self):
        """스케줄러 시작"""
        # 서버 시작 시 즉시 실행
        asyncio.create_task(self.collect_jobs())
        
        # 매일 새벽 3시에 채용 정보 수집
        self.scheduler.add_job(
            self.collect_jobs,
            CronTrigger(hour=3, minute=0),
            id="collect_jobs",
            replace_existing=True
        )
        
        # 매일 새벽 4시에 훈련 프로그램 수집
        self.scheduler.add_job(
            self.collect_training_programs,
            CronTrigger(hour=4, minute=0),
            id="collect_training_programs",
            replace_existing=True
        )
        
        # 매일 오전 9시와 오후 6시에 코드 데이터 수집
        self.scheduler.add_job(
            self.collect_codes,
            CronTrigger(hour='9,18', minute=0),
            id="collect_codes",
            replace_existing=True
        )
        
        self.scheduler.start()
    
    def get_status(self):
        """수집 상태 조회"""
        return {
            "jobs": {
                **self.collection_status["jobs"],
                "last_collection": self.last_job_collection.isoformat() if self.last_job_collection else None
            },
            "training": {
                **self.collection_status["training"],
                "last_collection": self.last_training_collection.isoformat() if self.last_training_collection else None
            },
            "codes": {
                **self.collection_status["codes"],
                "last_collection": self.last_code_collection.isoformat() if self.last_code_collection else None
            }
        } 