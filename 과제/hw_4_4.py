#보유중인 도서
list_of_book = [
    '장화홍련전',
    '가락국 신화',
    '온달 설화',
    '금오신화',
    '이생규장전',
    '만복자서포기',
    '수성지',
    '백호집',
    '원생몽유록',
    '홍길동전',
    '장생전',
    '도문대작',
    '옥루몽',
    '옥련몽',
]

#대여 예정 도서
rental_book = [
    '장생전',
    '위대한 개츠비',
    '원생몽유록',
    '이생규장전',
    '데미안',
    '장화홍련전',
    '수성지',
    '백호집',
    '난중일기',
    '홍길동전',
    '만복자서포기',
]

#리스트 컴프리헨션
#새로운_리스트 = [넣을값 for 변수 in 기존 리스트]
missing_book = [
    book
    for book in rental_book
    if book not in list_of_book
]

print(missing_book)


# if missing_book not in list_of_book:
#     print(f"{missing_book}을/를 보충하여야 합니다.")
# 만약 missing_book 이라면 프린트 -> missing book 아니면 대여 가능
# missingbook 개수가 0개 이상이라면? -> 보충해야함

# if missing_book: -> 이거는 list여서 맞는 말이긴 하지만 좀 불친절띠

# if missing_book != []: -> []이 아니라면! 이렇게 써도 됨


if len(missing_book) > 0:
    for book in missing_book:
        print(f"{book}을/를 보충하여야 합니다.")


else:
    print("모든 도서가 대여 가능한 상태입니다.")