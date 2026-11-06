import sys
sys.stdin = open('input.txt')

# portals : 각 방에서 왼쪽 포탈을 타면 어느 방으로 이동하는지 저장한 리스트 [0, 0, 1, 1, 2, 0]
# visit_counts : 각 방을 몇번 방문햇는지 기록한 리스트 [0, 0, 0, 0, 0, 0]
# current_room : 현재 내가 있는 방 번호
# next_room : 다음에 이동할 방 번호
# portal_uses : 지금까지 포탈을 사용한 총 횟수

T = int(input())
for tc in range(1, T + 1):
    N = int(input()) 
    portals = [0] + list(map(int, input().split()))
    # 굳이 0 을 하나 더 붙이는 이유 : 파이썬의 리스트는 인덱스가 0부터 시작하지만, 문제의 방 번호는 1부터 시작하기 때문
    # [0]을 붙이면 방 번호와 리스트 인덱스가 똑같아짐

    visit_counts = [0] * (N + 1) 
    # 각 방에 몇번 들어갔는지 기록하기 위한 리스트를 만드는거임


    current_room = 1 # 내가 지금 몇 번 방에 있는지 저장하는 변수. 문제에서 1번방에서 출발한다고 했으니까 처음에는 1을 저장
    portal_uses = 0 # 포탈을 몇번 사용했는지 세는 변수. 아직 출발하지 않아서 0으로 시작함

    while current_room < N: # 마지막 방에 도착할 때 까지 계속 이동하라는 뜻. N이 5가 되면 종료
        portal_uses += 1 # 그리고 반복할 때 마다 포탈을 한번 사용하니까 portal_uses += 1 을 실행

        if current_room == 1: # 현재 1번방에 있음? 현재 1번방이라면 무조건 2번방으로 이동해야해서 next_room =2인거임
            next_room = 2

        else:
            visit_counts[current_room] += 1 # 현재 1번방이 아니라몀, 그 방의 방문 횟수를 1 증가시켜라

            if visit_counts[current_room] == 1: # 현재 방에 처음 방문했는지 확인
                next_room = portals[current_room] # 다시 1번방으로 돌아감

            else:
                next_room = current_room + 1 # 현재 방에서 바로 오른쪽 방으로 이동해라

        current_room = next_room # 다음에 갈 방을 현재 방으로 바꾼다

    print(f'#{tc} {portal_uses}')