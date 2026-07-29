import json  # JSON 파일을 처리하기 위한 라이브러리
from pathlib import Path  # 파일 경로를 처리하기 위한 라이브러리


# 1. books_2000.json 파일 경로 설정
file_path = Path('skeleton') / 'data' / 'books_2000.json'

# 2. 생성할 JSON 파일 경로 설정
output_path = Path('skeleton') / 'category_books.json'

# 3. 파일 존재 여부 확인
if file_path.exists():

    # 4. books_2000.json 파일 읽기
    with file_path.open('r', encoding='utf-8') as file:
        books = json.load(file)

    # 카테고리별 도서 정보를 저장할 딕셔너리
    category_books = {}

    # 5. 전체 도서를 하나씩 순회
    for book in books:
        category_id = str(book['categoryId'])
        category_name = book['categoryName']

        # 처음 등장한 카테고리라면 기본 구조 생성
        if category_id not in category_books:
            category_books[category_id] = {
                'name': category_name,
                'books': [],
            }

        # 필요한 도서 정보만 새로운 딕셔너리로 정리
        book_info = {
            'title': book['title'],
            'author': book['author'],
            'publisher': book['publisher'],
            'pubDate': book['pubDate'],
            'isbn': book['isbn'],
            'price': book['priceSales'],
        }

        # 해당 카테고리의 books 리스트에 도서 정보 추가
        category_books[category_id]['books'].append(book_info)

    # 6. 정리한 데이터를 새로운 JSON 파일로 저장
    with output_path.open('w', encoding='utf-8') as file:
        json.dump(
            category_books,
            file,
            ensure_ascii=False,
            indent=4,
        )

    print(f'JSON 파일이 생성되었습니다: {output_path.name}')

else:
    print(f'파일이 존재하지 않습니다: {file_path}')