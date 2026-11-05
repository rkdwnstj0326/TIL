# import sys
# sys.stdin = open(" ")

# T = int(input())

# FROM = 16
# TO = 2
# GROUP = 1
# WIDTH = 4

# for tc in range(1, T + 1):
#     result = ""

#     hex_text_list = input().split()
#     for hex_text in hex_text_list:
#         for i in range(0, int(len(hex_text_list[0])), GROUP):
#             h = hex_text[i:i+GROUP]

#             integer = int(h, FROM)
#             binary = format(integer, {2:'b', 8:'o', 10:'d', 16:'X'}[TO])
#             result += binary.zfill(WIDTH)

#     len_hex_text_list = len(result)//2
#     right = result[len_hex_text_list:]
#     left = result[:len_hex_text_list]

#     count = 0
#     for k in range(len(left)):
#         if left[k] != right[k]:
#             count += 1

#     print(f'#{tc} {count}')




# import sys
# sys.stdin = open("")

# T = int(input())
# FROM = 16
# TO = 2
# GROUP = 1
# WIDTH = 4

# for tc in range(1, T + 1):
#     result = ""
#     hex_text_list = input().split()

#     for hex_text in hex_text_list:
#         for i in range(1, int(len(hex_text_list[0])), GROUP):
#             h = hex_text[i:i+GROUP]

#             integer = int(h, FROM)
#             binary = format(integer, {2:'b', 8:'o', 10:'d', 16:'X'}[TO])
#             result += binary.zfill(WIDTH)

#     len_hex_text_list = len(result)//2

#     left = result[:len_hex_text_list]
#     right = result[len_hex_text_list:]

#     count = 0
#     for k in range(len(left)):
#         if left[k] != right[k]:
#             count += 1
#     print(f'{tc} {count}')


import sys
sys.stdin = open("")

T = int(input())

FROM = 16
TO = 2
GROUP = 1
WIDTH = 4

for tc in range(1, T + 1):
    result = ""

    hex_text_list = input().split()

    for hex_text in hex_text_list:
        for i in range(0, int(len(hex_text_list[0])), GROUP):
            h = hex_text[i:i+GROUP]

            integer = int(h, FROM)
            binary = format(integer, {2:'b', 8:'o', 10:'d', 16:'X'}[TO])
            result += binary.zfill(WIDTH)

    len_hex_text_list = len(result)//2
    left = result[:len_hex_text_list]
    right = result[len_hex_text_list:]

    count = 0

    for k in range(len(left)):
        if left[k] != right[k]:
            count = count + 1

    print(f'#{tc} {count}')

import sys
sys.stdin = open("")

T = int(input())

# FROM = 16
# TO = 2
# GROUP = 1
# WIDTH = 4

# for tc in range(1, T + 1):
#     result = ""

#     hex_text_list = input().split()

#     for hex_text in hex_text_list:
#         for i in range(0, int(len(hex_text_list[0])), GROUP):
#             h = hex_text[i:i+GROUP]

#             integer = int(h, FROM)
#             binary = format(integer, {2:'b', 8:'o', 10:'d', 16:'X'}[TO])
#             result = binary.zfill[WIDTH]

#     len_hex_text_list = len(result)//2
#     left = result[:len_hex_text_list]
#     right = result[len_hex_text_list:]

#     count = 0

#     for k in range(len(left)):
#         if left[k] != right[k]:
#             count = count + 1

#     print

import sys
sys.stdin = open("")

T = int(input())

FROM = 16
TO = 2
GROUP = 1
WIDTH = 4

for tc in range(1, T + 1):
    result = ""
    hex_text_list = input().split()

    for hex_text in hex_text_list:
        for i in range(0, int(len(hex_text_list[0]), GROUP)):
            h = hex_text[i:i+GROUP]

            integer = int(h, FROM)
            binary = format(integer, {}[TO])
            result = binary.zfill(WIDTH)

    len_hex_text_list = len(result)//2
    left = result[:len_hex_text_list]
    right = result[len_hex_text_list:]

    count = 0

    for k in range(len(left)):
        if left[k] != right[k]:
            count += 1

    print

