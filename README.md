1. 가상환경 생성
먼저, 프로젝트의 루트 디렉토리에서 아래 명령어를 입력하여 가상환경을 생성합니다.

bash
복사
python -m venv venv
이 명령어는 venv라는 이름의 가상환경을 생성합니다.
2. 가상환경 활성화
가상환경을 활성화하려면 아래 명령어를 실행합니다.

Windows (명령 프롬프트):

bash
복사
venv\Scripts\activate
Windows (PowerShell):

bash
복사
.\venv\Scripts\Activate.ps1
Git Bash 또는 Unix-based 시스템 (Linux/Mac):

bash
복사
source venv/Scripts/activate
가상환경이 성공적으로 활성화되면, 프롬프트에 (venv)라는 표시가 나타납니다.

3. 필수 라이브러리 설치
가상환경이 활성화된 상태에서 프로젝트에 필요한 라이브러리들을 설치합니다.

bash
복사
pip install selenium chromedriver_autoinstaller
selenium: 웹 자동화를 위한 라이브러리
chromedriver_autoinstaller: 크롬 웹드라이버를 자동으로 설치하는 라이브러리
4. .gitignore
venv 폴더는 Git에서 추적하지 않도록 .gitignore 파일에 자동으로 추가됩니다. 이 파일은 이미 가상환경과 관련된 항목을 제외하도록 설정되어 있습니다.
