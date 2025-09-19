import time
from simpleai.search import CspProblem, backtrack
from collections import deque

# --- Đếm số lần kiểm tra ràng buộc ---
constraint_calls = 0

def queens_constraint(variables, values):
    """
    Ràng buộc N-Queens: không cùng cột và không cùng đường chéo.
    """
    global constraint_calls
    constraint_calls += 1
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] == values[j] or abs(i - j) == abs(values[i] - values[j]):
                return False
    return True

# --- AC3 cho simpleai ---
def ac3_simpleai(problem):
    queue = deque((xi, xj) for xi in problem.variables for xj in problem.variables if xi != xj)
    while queue:
        xi, xj = queue.popleft()
        if revise(problem, xi, xj):
            if not problem.domains[xi]:
                return False
            for xk in problem.variables:
                if xk != xi and xk != xj:
                    queue.append((xk, xi))
    return True

def revise(problem, xi, xj):
    revised = False
    to_remove = set()
    for x in problem.domains[xi]:
        # Kiểm tra xem có giá trị nào ở xj thỏa mãn ràng buộc không
        if not any(queens_constraint([xi, xj], [x, y]) for y in problem.domains[xj]):
            to_remove.add(x)
            revised = True
    problem.domains[xi] = [v for v in problem.domains[xi] if v not in to_remove]
    return revised

# --- Hàm giải N-Queens ---
def solve_nqueens(n, use_ac3=False):
    global constraint_calls
    constraint_calls = 0
    variables = list(range(n))
    domains = {v: list(range(n)) for v in variables}
    constraints = [(variables, queens_constraint)]
    problem = CspProblem(variables, domains, constraints)

    if use_ac3:
        ac3_simpleai(problem)

    start = time.time()
    result = backtrack(problem)
    end = time.time()
    return result, end - start, constraint_calls

# --- Hàm in bàn cờ ---
def print_board(solution, n):
    for r in range(n):
        row = ''
        for c in range(n):
            row += 'Q ' if solution[r] == c else '. '
        print(row)

# --- Main ---
if __name__ == "__main__":
    print("--- N-Queens (N=5) CSP: So sánh Backtracking và Backtracking + AC3 ---")
    for ac3_flag in [False, True]:
        result, t, steps = solve_nqueens(5, use_ac3=ac3_flag)
        print(f"\nAC3 = {ac3_flag}: {result}")
        print(f"Time: {t:.4f}s, Constraint calls: {steps}")
        print("Bàn cờ:")
        print_board(result, 5)
