import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. JSON 파일 로드
json_file_path = "jobs.json"

with open(json_file_path, "r", encoding="utf-8") as file:
    jobs_data = json.load(file)

# 2. JSON 데이터를 Pandas DataFrame으로 변환
df = pd.DataFrame(jobs_data)

# 데이터 확인
print(df.head())

# 3. 특성(features)과 레이블(label) 분리
# 예: 레이블로 "salary" 범주화를 사용
# salary를 100,000 이상/미만으로 이진 분류
df['salary_category'] = df['salary'].apply(lambda x: 1 if x >= 100000 else 0)

# 특성(features) 선택 (title과 location의 길이 예시)
df['title_length'] = df['title'].apply(len)
df['location_length'] = df['location'].apply(len)

# 입력 데이터와 출력 데이터 분리
X = df[['title_length', 'location_length']]
y = df['salary_category']

# 4. 학습용 및 테스트용 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. 모델 학습
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 6. 모델 평가
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"모델 정확도: {accuracy * 100:.2f}%")

# 7. 추천 결과 생성
def recommend_jobs(data, model):
    data['score'] = model.predict_proba(data[['title_length', 'location_length']])[:, 1]
    return data.sort_values('score', ascending=False)

# 테스트 데이터에서 추천 순서 정렬
recommended_jobs = recommend_jobs(df, model)

print("추천된 공고:")
print(recommended_jobs[['title', 'location', 'link']])
