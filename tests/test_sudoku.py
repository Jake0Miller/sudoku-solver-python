from sudoku import sudoku
from seeds import seeds
import pdb

index = 0
run = 0
success = 0
for board, solution in zip(seeds.boards, seeds.solutions):
    index += 1
    for solved in sudoku.solve_sudoku((3, 3), board):
        run += 1
        if solved == solution:
            print(f"Test {index} passed!")
            success += 1
        else:
            print(f"Test {index} failed!")

print(f"{run}/{len(seeds.boards)} tests ran!")
print(f"{success}/{len(seeds.boards)} succeeded!")
