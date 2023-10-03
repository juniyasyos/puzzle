from collections import deque
import copy

def display_moves(moves, puzzle_show):
    print("\nInitial Puzzle_show:")
    for row in puzzle_show:
        print(row)

    if moves:
        print("\nSequence of Moves:")
        for move in moves:
            x, y = move[0], move[1]
            print("\n")
            print(" " * 10, " : ", puzzle_show[0])
            print(" " * 10, " : ", puzzle_show[1])
            print(" " * 10, " : ", puzzle_show[2])

def bfs_solve(initial_state, target_state):
    visited = set()
    queue = deque([(initial_state, [])])  # Menyimpan keadaan dan path

    while queue:
        current_state, path = queue.popleft()

        if current_state == target_state:
            return path  # Solusi ditemukan

        visited.add(tuple(map(tuple, current_state)))

        # Menghasilkan langkah-langkah yang mungkin
        zero_pos = (0, 0)
        for i in range(3):
            for j in range(3):
                if current_state[i][j] == 0:
                    zero_pos = (i, j)

        moves = []
        if zero_pos[0] > 0:
            moves.append((-1, 0, 'UP'))
        if zero_pos[0] < 2:
            moves.append((1, 0, 'DOWN'))
        if zero_pos[1] > 0:
            moves.append((0, -1, 'LEFT'))
        if zero_pos[1] < 2:
            moves.append((0, 1, 'RIGHT'))

        for move in moves:
            dx, dy, move_name = move
            x, y = zero_pos[0] + dx, zero_pos[1] + dy
            new_state = [list(row) for row in current_state]  # Konversi ke list untuk memodifikasi
            new_state[zero_pos[0]][zero_pos[1]], new_state[x][y] = new_state[x][y], new_state[zero_pos[0]][zero_pos[1]]
            new_state = tuple(map(tuple, new_state))  # Konversi kembali ke tuple setelah modifikasi
            if new_state not in visited:
                queue.append((new_state, path + [move_name]))

    return None  # Tidak ada solusi

# Keadaan awal dan tujuan
initial_state = (
    (2, 4, 3),
    (1, 5, 6),
    (7, 0, 8)
)

target_state = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

# Menyelesaikan teka-teki
solution = bfs_solve(initial_state, target_state)

if solution:
    print("Langkah-langkah untuk menyelesaikan teka-teki:")
    display_moves(solution, initial_state)
else:
    print("Tidak ada solusi.")
