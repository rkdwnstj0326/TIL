import sys
sys.stdin = open("algo1_sample_in.txt")

T = int(input())

FROM = 16
TO = 2
GROUP = 1
WIDTH = 4

for tc in range(1, T + 1):
    result = ""
    
    hex_text_list = list(input().split())
    
    # print(len(hex_text_list[0]))
    for hex_text in hex_text_list:
        for i in range(0, int(len(hex_text_list[0])), GROUP):
            h = hex_text[i:i+GROUP]
    # 여기까지

            integer = int(h, FROM)
            binary = format(integer, {2:'b', 8:'o', 10:'d', 16:'X'}[TO])
            result += binary.zfill(WIDTH)

    # print(result)

    len_hex_text_list = len(result) // 2
    left_hex_text = result[:len_hex_text_list]
    right_hex_text = result[len_hex_text_list:]

    count_diff = 0

    for k in range(len(left_hex_text)):
        if left_hex_text[k] != right_hex_text[k]:
            count_diff += 1

    # if left_hex_text == right_hex_text:


    print(f'#{tc} {count_diff}')

