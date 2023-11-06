import copy

def display_moves(moves,puzzle_show,initial_pcc):
    x, y = initial_pcc[0],initial_pcc[1]

    print("\nInitial Puzzle_show:")
    for row in puzzle_show:
        print(row)

    print("\nSequence of Moves:")
    for move in moves:
        if move == 'UP':
            puzzle_show[x][y], puzzle_show[x - 1][y] = puzzle_show[x - 1][y], puzzle_show[x][y]
            x -= 1
        elif move == 'DOWN':
            puzzle_show[x][y], puzzle_show[x + 1][y] = puzzle_show[x + 1][y], puzzle_show[x][y]
            x += 1
        elif move == 'LEFT':
            puzzle_show[x][y], puzzle_show[x][y - 1] = puzzle_show[x][y - 1], puzzle_show[x][y]
            y -= 1
        elif move == 'RIGHT':
            puzzle_show[x][y], puzzle_show[x][y + 1] = puzzle_show[x][y + 1], puzzle_show[x][y]
            y += 1

        print("\n")
        print(" ".ljust(10)," : ",puzzle_show[0])
        print(move.ljust(10)," : ",puzzle_show[1])
        print(" ".ljust(10)," : ",puzzle_show[2])

def solve_puzzle(puzzle, target_puzzle, pcc, stack=0, limit=10, path=None):
    def valid(x, y):
        if 0 <= x < 3 and 0 <= y < 3:
            return True
        return False

    def is_opposite(move1, move2):
        if (move1 == "UP" and move2 == "DOWN") or \
        (move1 == "DOWN" and move2 == "UP") or \
        (move1 == "LEFT" and move2 == "RIGHT") or \
        (move1 == "RIGHT" and move2 == "LEFT"):
            return True
        return False
    
    if puzzle == target_puzzle:
        return stack, path, "Jalur terdekat ditemukan"
    if stack == limit:
        return stack, path, "Tidak ditemukan jalur terdekat"

    new_puzzle = copy.deepcopy(puzzle)
    move = [["UP", [-1, 0]], ["DOWN", [1, 0]], ["LEFT", [0, -1]], ["RIGHT", [0, 1]]]
    valid_move = [False, False, False, False]

    for i in range(len(valid_move)):
        new_x, new_y = move[i][1][0] + pcc[0], move[i][1][1] + pcc[1]
        if valid(new_x, new_y) and (path is None or not is_opposite(path[-1], move[i][0])):
            valid_move[i] = True

    save_result = []
    for i in range(len(valid_move)):
        if valid_move[i]:
            if path is None:
                new_moving = [move[i][0]]
            else:
                new_moving = path + [move[i][0]]

            new_puzzle[pcc[0]][pcc[1]], new_puzzle[move[i][1][0] + pcc[0]][move[i][1][1] + pcc[1]] = new_puzzle[move[i][1][0] + pcc[0]][move[i][1][1] + pcc[1]], new_puzzle[pcc[0]][pcc[1]]
            result = solve_puzzle(new_puzzle, target_puzzle, [move[i][1][0] + pcc[0], move[i][1][1] + pcc[1]], stack=stack + 1, path=new_moving,limit=limit)
            save_result.append(result)
            new_puzzle[pcc[0]][pcc[1]], new_puzzle[move[i][1][0] + pcc[0]][move[i][1][1] + pcc[1]] = new_puzzle[move[i][1][0] + pcc[0]][move[i][1][1] + pcc[1]], new_puzzle[pcc[0]][pcc[1]]

    for i in range(len(save_result)):
        if save_result[i][0] == None and save_result[i][0] == limit:
            continue
        elif save_result[i][0] == min([j[0] for j in save_result]):
            return save_result[i]

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

for i in range(len(puzzle)):
    for j in range(len(puzzle[0])):
        if puzzle[i][j] == 0:
            initial_position = [i, j]

print("\nInitial move : ", initial_position)
print("\nPuzzle Target: ")
for i in target_puzzle:
    print(i)

print("\nInitial Puzzle: ")
for i in puzzle:
    print(i)

result = solve_puzzle(puzzle,target_puzzle,initial_position,limit=35)

print("\nPesan ['", result[2], "']")
print("\nMinimum number of moves:", result[0])
print("Sequence of moves:", result[1])


    # Menampilkan perpindahan
if result[2] != "Tidak ditemukan jalur terdekat":
    display_moves(result[1],puzzle,initial_position)