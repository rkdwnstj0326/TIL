from datetime import datetime  # 날짜와 시간을 처리하기 위한 라이브러리
import json  # JSON 파일을 처리하기 위한 라이브러리
from pathlib import Path  # 파일 경로를 처리하기 위한 라이브러리

# 월별 책 정보 모아보고 평균 가격 계산하기
# 아래에 전체 코드 작성

# 1.파일 경로 설정
file_path = Path('./skeleton/data/books_2000.json')

# 2.파일 존재 여부 확인
if file_path.exists():

    #Json 파일 열기
    with file_path.open('r',encoding='utf-8') as file:
        data = json.load(file)

    # 3. 월별 가격 정보를 저장할 딕셔너리 생성
    monthly_prices = {}

    # 모든 도서 정보를 순회
    for item in data:

        # 출판일을 datetime 객체로 변환
        pub_date = datetime.strptime(item['pubDate'], "%Y-%m-%d")

        # 월만 추출 (1~12)
        month = pub_date.month

        # 판매 가격 가져오기
        price = item['priceSales']

        # 해당 월이 없으면 빈 리스트 생성
        if month not in monthly_prices:
            monthly_prices[month] = []

        # 해당 월에 가격 추가
        monthly_prices[month].append(price)

    # 4. 월별 평균 가격 계산 및 출력

    print("월별 평균 가격 및 도서 수:")

    for month in sorted(monthly_prices.keys()):
        prices = monthly_prices[month]
        average_price = sum(prices) / len(prices)

        print(f"{month}월: 평균 가격 {average_price:.2f}원 (총 {len(prices)}권)")
else:
    # 파일이 존재하지 않을 경우
    print(f"파일이 존재하지 않습니다: {file_path}")