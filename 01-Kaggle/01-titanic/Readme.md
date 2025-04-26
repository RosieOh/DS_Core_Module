# 🐼 Pandas 숫자 포맷 설정 완전 마스터 가이드

## 🎯 display.precision 으로 소수점 자리수 조정하기
display.float_format 없이,
간단하게 소수점 자리수만 조정하고 싶을 때는 display.precision 옵션을 쓰면 된다.

```python
pd.set_option('display.precision', 4)
```

✅ 이렇게 하면 모든 float 숫자가 자동으로 소수점 4자리까지 표시된다!

### ✨ 예시
```python
import pandas as pd


# 데이터 불러오기
data = pd.read_csv('http://bit.ly/ld-sample-idol', index_col='순위')

# 소수점 4자리까지 표시 설정
pd.set_option('display.precision', 4)

# 데이터 확인
print(data.head())
```

### 🔎 출력 예시:

|이름|그룹|총득표수|
|----|---|----|
|지민|	BTS|6747437.0000|
|정국|	BTS|5923568.0000|
|뷔|	BTS|	5305517.0000|

### 🚀 precision vs float_format 차이
|항목|	display.precision|	display.float_format|
|--|--|--|
|포맷 제어 수준|	단순 소수점 자리수|	포맷을 자유롭게 (쉼표, 단위, 포맷 스타일 가능)
|사용 예시|	소수점 자리만 고정	|천 단위 쉼표 + 소수점|
|코드 예|	pd.set_option('display.precision', 2)	|pd.set_option('display.float_format', lambda x: f'{x:,.2f}')|

> ✅ 간단한 자리수 조정 ➔ precision<br/>✅ 포맷팅 꾸미기 ➔ float_format

### 🛠 옵션 리셋도 잊지 말자
설정한 옵션은 아래처럼 리셋 가능:

```python
# precision 리셋
pd.reset_option('display.precision')
```

### 📚 참고 링크
Pandas Display Options 공식 문서

Python Format Mini-Language

