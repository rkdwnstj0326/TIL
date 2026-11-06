# # import sys
# # sys.stdin = open('input.txt')

# # T = int(input())
# # for tc in range(1, T + 1):
# #     N = int(input())
# #     portals = [0] + list(map(int, input().split()))

# #     visit_counts = [0] * (N + 1)

# #     current_room = 1
# #     portal_uses = 0

# #     while current_room < N:
# #         portal_uses += 1

# #         if current_room == 1:
# #             next_room = 2

# #         else:
# #             visit_counts[current_room] += 1

# #             if visit_counts[current_room] == 1:
# #                 next_room = portals[current_room]

# #             else:
# #                 next_room = current_room + 1

# #         current_room = next_room

# #     print(f'#{tc} {portal_uses}')

# # import sys
# # sys.stdin = open('input.txt')

# # T = int(input())

# # for tc in range(1, T + 1):
# #     N = int(input())
# #     portals = [0] + list(map(int, input().split()))

# #     visit_counts = [0] * (N + 1)

# #     current_room = 1
# #     portal_uses = 0

# #     while current_room < N:
# #         portal_uses += 1

# #         if current_room == 1:
# #             next_room = 2

# #         else:
# #             visit_counts[current_room] += 1

# #             if visit_counts[current_room] == 1:
# #                 next_room = portal_uses[current_room]

# #             else:
# #                 next_room = current_room + 1

# #         current_room = next_room
# #     print(f'#{tc} {portal_uses}')



# T = int(input())
# for tc in range(1, T + 1):
#     N = int(input())
#     portals = [0] + list(map(int, input().split()))

#     visit_counts = [0] * (N + 1)

#     current_room = 1
#     portal_uses = 0

#     while current_room < N:
#         portal_uses += 1

#         if current_room == 1:
#             next_room = 2

#         else:
#             visit_counts[current_room] += 1

#             if visit_counts[current_room] == 1:
#                 next_room = portals[current_room]

#             else:
#                 next_room = current_room + 1

#         current_room = next_room

#     print(f'#{tc} {portal_uses}')



T = int(input())

for tc in range(1, T + 1):
    N = int(input())
    portals = [0] + list(map(int, input().split()))

    visit_counts = [0] * (N + 1)

    current_room = 1
    portal_uses = 0

    while current_room < N:
        portal_uses += 1

        if current_room == 1:
            next_room = 2

        else:
            visit_counts[current_room] += 1

            if visit_counts[current_room] == 1:
                next_room = portals[current_room]

            else:
                next_room = current_room + 1

        current_room = next_room













































