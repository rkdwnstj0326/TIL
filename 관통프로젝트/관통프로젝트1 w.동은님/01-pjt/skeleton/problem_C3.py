from pathlib import Path
import json

# 시리즈 정보가 있는 책들 끼리 묶기
# 아래에 생성형 AI를 활용한 코드 작성
series_data = {}

series_path = Path('./data/series_items')

for json_file in series_path.rglob('*.json'):
    with json_file.open('r', encoding='utf-8') as file:
        data = json.load(file)

    # 파일 구조가 dict인 경우(item 키 사용)
        book = data

        if 'seriesInfo' not in book:
            continue

        info = book['seriesInfo']

        series_id = str(info['seriesId'])

        if series_id not in series_data:
            series_data[series_id] = {
                'seriesId': info['seriesId'],
                'seriesName': info['seriesName'],
                'books': []
            }

        series_data[series_id]['books'].append(book)

output_path = Path('./data/series.json')

with output_path.open('w', encoding='utf-8') as file:
    json.dump(series_data, file, ensure_ascii=False, indent=4)

print("모든 시리즈 데이터가 series.json 파일로 병합되었습니다.")
