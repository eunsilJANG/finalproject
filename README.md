## 가상환경 세팅
### 1. 가상환경 생성
python -m venv venv
### 2. 가상환경 활성화
venv\Scripts\activate
### 3. 필수 라이브러리 설치
pip install selenium chromedriver_autoinstaller

## .gitignore 파일
`venv` 폴더는 가상환경을 생성할 때 **자동으로 `.gitignore`**에 추가됨.
### created by virtualenv automatically
venv/
