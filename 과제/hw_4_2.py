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

rental_list = [
    '장생전',
    '원생몽유록',
    '이생규장전',
    '장화홍련전',
    '수성지',
    '백호집',
    '난중일기',
    '홍길동전',
    '만복자서포기',
]

# for book in list_of_book :
#     for rental in rental_list :
#         print(f"{book}은/는 보유하고 있지 않습니다.")

# rental_list를 하나씩 확인하다가 보유하지 않은 책을 발견하면 출력하고 즉시 반복 끝내야 함
# for 변수 in 반복할 자료


for book in rental_list :
    if book not in list_of_book:
        print(f"{book}은/는 보유하고 있지 않습니다.")

        break

else :
    print('모든 도서가 대여 가능한 상태입니다.')

