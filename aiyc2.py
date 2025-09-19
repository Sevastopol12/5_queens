import time

N = 5  # số hậu (chỉ 5 quân hậu)

# --- Hàm kiểm tra ràng buộc ---
def is_safe(solution, row, col):
    for r, c in enumerate(solution):
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

# --- Hàm in bàn cờ ---
def print_board(solution):
    for r in range(N):
        row = ""
        for c in range(N):
            if r < len(solution) and solution[r] == c:
                row += " Q "
            else:
                row += " . "
        print(row)
    print("-" * (3 * N))

# --- Chiến lược 1: Backtracking cơ bản (chọn hàng theo thứ tự) ---
def backtrack_basic(row=0, solution=None, solutions=None):
    if solution is None:
        solution, solutions = [], []
    if row == N:
        solutions.append(solution[:])
        return solutions
    for col in range(N):
        if is_safe(solution, row, col):
            solution.append(col)
            backtrack_basic(row+1, solution, solutions)
            solution.pop()
    return solutions

# --- Chiến lược 2: MRV (chọn hàng có ít cột khả thi nhất) ---
def backtrack_mrv(solution=None, solutions=None):
    if solution is None:
        solution, solutions = [], []
    if len(solution) == N:
        solutions.append(solution[:])
        return solutions

    row = len(solution)
    domain = [c for c in range(N) if is_safe(solution, row, c)]

    if not domain:
        return solutions

    for col in domain:
        new_sol = solution[:] + [col]
        backtrack_mrv(new_sol, solutions)
    return solutions

# --- Chiến lược 3: LCV (chọn giá trị gây ít xung đột nhất) ---
def order_lcv(solution, row):
    def conflicts(col):
        count = 0
        for r in range(row+1, N):
            for c in range(N):
                if not is_safe(solution + [col], r, c):
                    count += 1
        return count
    return sorted(range(N), key=conflicts)

def backtrack_lcv(row=0, solution=None, solutions=None):
    if solution is None:
        solution, solutions = [], []
    if row == N:
        solutions.append(solution[:])
        return solutions
    for col in order_lcv(solution, row):
        if is_safe(solution, row, col):
            solution.append(col)
            backtrack_lcv(row+1, solution, solutions)
            solution.pop()
    return solutions

# --- Hàm chạy thử nghiệm ---
def run_solver(solver, name):
    start = time.time()
    sols = solver()
    end = time.time()
    print(f"{name}: {len(sols)} solutions found in {end-start:.4f}s")

    # In thử tối đa 3 nghiệm đầu
    for i, sol in enumerate(sols[:3], 1):
        print(f"Solution {i}: {sol}")
        print_board(sol)

# Thử nghiệm với các chiến lược
run_solver(backtrack_basic, "Basic Backtracking")
run_solver(backtrack_mrv,   "MRV")
run_solver(backtrack_lcv,   "LCV")
