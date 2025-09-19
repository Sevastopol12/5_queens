from constraint import Problem


# 5x5 board, 5 queens
N = 5

# 1. Define problem
problem = Problem()

# 2. Variables:
#    One variable per row, value = column index of queen in that row
rows = range(N)
columns = range(N)
problem.addVariables(rows, columns)

# 3. Constraints:
#    (a) All queens must be in different columns
problem.addConstraint(lambda *cols: len(set(cols)) == N, rows)

#    (b) No two queens on same diagonal
#        For any two different rows r1, r2:
def no_diagonal_conflict(c1, c2, r1, r2):
    return abs(c1 - c2) != abs(r1 - r2)

for r1 in rows:
    for r2 in rows:
        if r1 < r2:
            problem.addConstraint(
                lambda c1, c2, r1=r1, r2=r2: no_diagonal_conflict(c1, c2, r1, r2),
                (r1, r2)
            )

# 4. Solve
solutions = problem.getSolutions()

print(f"Number of solutions: {len(solutions)}")
for s in solutions:
    print(s)

# Optional: pretty print a board for each solution
def print_board(solution):
    for r in range(N):
        line = ""
        for c in range(N):
            line += "Q " if solution[r] == c else ". "
        print(line)
    print()

for sol in solutions:
    print_board(sol)