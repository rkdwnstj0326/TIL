# N개의 당근을 주문하면 대, 중, 소 상자로 구분해서 포장
# 같은 크기의 당근은 같은 상자에
# 비어있는 상자가 있으면 안됨
# 한 상자에 N/2개를 초과하는 당근이 있어서도 안됨
# 각 상자에 든 당근의 개수 차이가 최소가 되도록 포장

import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    carrots = list(map(int, input().split()))

    # 당근을 크기순으로 정렬
    carrots.sort()

    # 정답을 저장할 변수 만들기. answer은 '가장 작은 개수 차이'를 저장할 변수. 아직 포장에 성공안해서 -1로 둠 그리고 0은 실제로 나올 수 있음 그래서 -1
    answer = -1

    # 소 상자에 담을 당근 개수 : i
    for i in range(1, N - 1):
        # 같은 크기의 당근은 나누면 안됨. so 같은 크기의 당근 확인하기
        if carrots[i - 1] == carrots[i]: # 앞의 당근이랑 뒤의 당근이랑 숫자 같으면 건너뗘라~
            continue

        # 소 + 중 상자에 담을 당근 개수
        for j in range(i + 1, N):
            # 같은 크기의 당근은 나누면 안됨
            if carrots[j - 1] == carrots[j]:
                continue

            # 각 상자의 당근 개수
            small = i
            medium = j - i
            large = N - j

            # 한 상자에 N//2개 초과하면 안된다
            if small > N // 2:
                continue
            if medium > N // 2:
                continue
            if large > N // 2:
                continue

            # 가장 많은 상자 - 가장 적은 상자
            diff = max(small, medium, large) - min(small, medium, large)

            # 최소 차이 저장
            if answer == -1:
                answer = diff
            elif diff < answer:
                answer = diff
    print(f'#{tc} {answer}')
    