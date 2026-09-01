"""
카운팅 정렬 (Counting Sort) - 실습 스켈레톤

목표: 주석의 힌트를 보고 빈 줄(TODO)을 직접 채워 완성하기!

개념 복습
  - 값끼리 '비교'하지 않는다. 각 숫자가 몇 번 나왔는지 '빈도수'만 센다.
  - 비유: '줄 세우기'가 아니라 '투표함 분류하기'.
          숫자가 적힌 상자(Index)에 표(Data)를 넣었다가 순서대로 꺼낸다.
  - 3단계: (1) 빈도수 세기 -> (2) 누적 합 -> (3) 뒤에서부터 배치

시간 복잡도: O(n + k)
공간 복잡도: O(k)
"""


def counting_sort(input_arr, k):
    """
    input_arr: 정렬할 리스트
    k: 데이터의 최대값 (범위)
    """

    # [실습 포인트 1] 카운팅 배열 만들기
    #   힌트) 숫자의 '값'을 그대로 인덱스로 쓸 것이다. 0부터 k까지 담으려면 몇 칸이 필요할까?
    #   힌트) [0] * 칸수
    # TODO: counting_arr = ____
    counting_arr = [0] * (k + 1)

    # [실습 포인트 2] 빈도수 기록
    #   힌트) input_arr를 한 번 훑으면서, 그 숫자에 해당하는 칸을 1씩 올린다.
    # TODO: for num in input_arr:
    #           ____
    for num in input_arr:
        counting_arr[num] += 1

    # [실습 포인트 3] 누적 합 계산
    #   힌트) 앞칸의 값을 내 칸에 더한다. 이러면 각 칸은 "이 숫자가 들어갈 마지막 방 번호"가 된다.
    #   힌트) 0번 칸은 앞이 없으므로 1번 칸부터 시작!
    # TODO: for i in range(____, ____):
    #           ____
    for i in range(1, k + 1):
        counting_arr[i] += counting_arr[i - 1]

    # [실습 포인트 4] 결과 배열 만들기
    #   힌트) 원본과 같은 개수만큼 0으로 채운 리스트
    # TODO: result_arr = ____
    result_arr = [0] * len(input_arr)

    # [실습 포인트 5] 역순 순회 & 배치  ★ 이 실습의 하이라이트 ★
    #   힌트) 왜 reversed()일까? -> 같은 값이 여러 개일 때 '원래 순서'를 지키기 위해서(안정 정렬).
    #         앞에서부터 넣으면 먼저 온 값이 뒷자리로 밀려나 순서가 뒤집힌다.
    #   순서) (1) 누적 합에서 1을 뺀다 (0-index 보정)  (2) 그 위치에 값을 넣는다
    # TODO: for num in reversed(input_arr):
    #           ____   # 누적 합 -1
    #           ____   # result_arr의 해당 위치에 num 배치
    for num in reversed(input_arr):
        counting_arr[num] -= 1
        result_arr[counting_arr[num]] = num

    return result_arr


if __name__ == '__main__':
    # 테스트
    arr = [6, 2, 4, 0, 1, 1]
    # 최대값 k=6 (0~6 범위이므로 넉넉하게)
    print(f'정렬 결과: {counting_sort(arr, 6)}')
    # 출력: [0, 1, 1, 2, 4, 6]

    # print('\n--- 과정 추적 ---')
    # counting_sort_verbose(arr, 6)   


# ---------------------------------------------------------------------------
# 자주 하는 실수 체크리스트
#   1) 카운팅 배열을 [0] * k 로 만들면, 값이 k일 때 IndexError! -> k + 1 칸 필요.
#   2) 누적 합을 range(0, k + 1)로 돌리면 counting_arr[-1]을 참조해 값이 꼬인다. -> 1부터 시작.
#   3) reversed()를 빼고 앞에서부터 순회하면 결과는 정렬되지만 '안정성'이 깨진다.
#   4) 배치할 때 -= 1 을 빼먹으면 result_arr 범위를 벗어나거나 값이 덮어씌워진다.
#   5) 음수 데이터는 인덱스로 쓸 수 없다. (오프셋 보정 필요)
# ---------------------------------------------------------------------------


# def counting_sort_verbose(input_arr, k):
#     """[디버깅용] 각 단계의 배열 상태를 출력하는 버전."""
#     print(f'[입력] {input_arr} (k={k})')

#     counting_arr = [0] * (k + 1)

#     for num in input_arr:
#         counting_arr[num] += 1
#     print(f'  1) 빈도수 : {counting_arr}')

#     for i in range(1, k + 1):
#         counting_arr[i] += counting_arr[i - 1]
#     print(f'  2) 누적 합: {counting_arr}  <- "이 숫자가 들어갈 마지막 방 번호"')

#     result_arr = [0] * len(input_arr)

#     print('  3) 역순 배치')
#     for num in reversed(input_arr):
#         counting_arr[num] -= 1
#         result_arr[counting_arr[num]] = num
#         print(f'     값 {num} -> index {counting_arr[num]} | {result_arr}')

#     print(f'[출력] {result_arr}')
#     return result_arr
