import sys

sys.stdin = open("sample1_in.txt", "r")

T = int(input())

for tc in range(1, T+1):
    N = int(input())
    
    nums = list(map(int, input().split()))
    
    result = 1
    
    prev_num = nums[0]
    
    for i in range(1, N):
        current_num = nums[i]
        
        if prev_num > current_num:
            prev_num = current_num
            
        elif prev_num <= current_num:
            result = 0
            break
        
    print(f'#{tc} {result}')