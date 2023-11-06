from collections import deque
import copy

def display_puzzle(puzzle):
    for row in puzzle:
        print(" ".join(map(str, row)))

def solve_puzzle_bfs(puzzle, target_puzzle, pcc):
    def valid(x, y):
        return 0 <= x < 3 and 0 <= y < 3

    def is_solved(puzzle, target_puzzle):
        return puzzle == target_puzzle

    def apply_move(puzzle, move, pcc):
        x, y = pcc
        new_puzzle = copy.deepcopy(puzzle)
        if move == 'UP' and valid(x - 1, y):
            new_puzzle[x][y], new_puzzle[x - 1][y] = new_puzzle[x - 1][y], new_puzzle[x][y]
            return (new_puzzle, (x - 1, y))
        elif move == 'DOWN' and valid(x + 1, y):
            new_puzzle[x][y], new_puzzle[x + 1][y] = new_puzzle[x + 1][y], new_puzzle[x][y]
            return (new_puzzle, (x + 1, y))
        elif move == 'LEFT' and valid(x, y - 1):
            new_puzzle[x][y], new_puzzle[x][y - 1] = new_puzzle[x][y - 1], new_puzzle[x][y]
            return (new_puzzle, (x, y - 1))
        elif move == 'RIGHT' and valid(x, y + 1):
            new_puzzle[x][y], new_puzzle[x][y + 1] = new_puzzle[x][y + 1], new_puzzle[x][y]
            return (new_puzzle, (x, y + 1))
        return (new_puzzle, pcc)

    move = ["UP", "DOWN", "LEFT", "RIGHT"]
    queue = deque([(puzzle, [])])
    visited = set()

    while queue:
        current_puzzle, moves = queue.popleft()
        pcc = None

        # Temukan posisi kotak kosong (0)
        for i in range(3):
            for j in range(3):
                if current_puzzle[i][j] == 0:
                    pcc = (i, j)
                    break

        for m in move:
            new_puzzle, new_pcc = apply_move(current_puzzle, m, pcc)

            # Konversi puzzle ke tuple agar dapat digunakan sebagai kunci dalam set
            new_puzzle_tuple = tuple(map(tuple, new_puzzle))

            if new_puzzle_tuple not in visited:
                visited.add(new_puzzle_tuple)
                new_moves = moves + [m]

                if is_solved(new_puzzle, target_puzzle):
                    return new_moves

                queue.append((new_puzzle, new_moves))

    return None

target_puzzle = [
    [1, 2, 3],
    [6, 5, 4],
    [7, 8, 0]
]

# puzzle = generate_random_puzzle()
puzzle = [
    [1, 2, 3],
    [5, 8, 4],
    [6, 0, 7]
]


initial_position = (2, 1)  # Koordinat awal pcc

print("Initial Puzzle:")
display_puzzle(puzzle)

print("Puzzle Target:")
display_puzzle(target_puzzle)

print("Solving puzzle...")

solution = solve_puzzle_bfs(puzzle, target_puzzle, initial_position)

if solution:
    print("Solution found in", len(solution), "moves:")
    print(solution)
else:
    print("No solution found.")

# Initial Puzzle:
# 2 4 3
# 1 5 6
# 7 0 8
# Puzzle Target:
# 1 2 3
# 4 5 6
# 7 8 0
# Solving puzzle...
# Solution found in 7 moves:
# ['UP', 'UP', 'LEFT', 'DOWN', 'RIGHT', 'DOWN', 'RIGHT']