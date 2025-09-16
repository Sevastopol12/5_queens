import random
import math
import time
import pandas as pd


# Utility functions

def conflicts(board: list[int]) -> int:
    """
    Count number of conflicts in board assignment.
    board: list of length n, board[row] = column
    """
    n: int = len(board)
    count = 0
    for r1 in range(n):
        for r2 in range(r1 + 1, n):
            c1, c2 = board[r1], board[r2]
            if c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                count += 1
    return count


def random_board(n):
    """Generate a random board assignment."""
    return [random.randrange(n) for _ in range(n)]


# Hill Climbing

def hill_climbing(n=5, max_steps=1000) -> tuple[list[int], int]:
    board: list[int] = random_board(n)
    for step in range(max_steps):
        current_conf = conflicts(board)
        if current_conf == 0:
            return board, step
        # Generate neighbors (move one queen)
        neighbors = []
        for row in range(n):
            for col in range(n):
                if col != board[row]:
                    new_board = board[:]
                    new_board[row] = col
                    neighbors.append(new_board)
        # Choose neighbor with lowest conflict
        next_board = min(neighbors, key=conflicts)
        if conflicts(next_board) >= current_conf:
            # local optimum
            return board, step
        board = next_board
    return board, max_steps


# Simulated Annealing

def simulated_annealing(n=5, max_steps=1000, T=1.0, cooling=0.99) -> tuple[list[int], int]:
    board: list[int] = random_board(n)
    for step in range(max_steps):
        current_conf: int = conflicts(board)
        if current_conf == 0:
            return board, step
        row: int = random.randrange(n)
        col: int = random.randrange(n)
        new_board = board[:]
        new_board[row] = col
        delta = conflicts(new_board) - current_conf
        if delta < 0 or random.random() < math.exp(-delta / T):
            board = new_board
        T *= cooling
    return board, max_steps


# Genetic Algorithm

def genetic_algorithm(n=5, pop_size=50, generations=500, mutation_rate=0.2) -> tuple[list[int], int]:
    def fitness(board):
        return -conflicts(board)  # maximize negative conflicts

    # Initialize population
    population = [random_board(n) for _ in range(pop_size)]

    for gen in range(generations):
        # Evaluate
        scored = [(fitness(b), b) for b in population]
        scored.sort(reverse=True)
        best_score, best_board = scored[0]
        if conflicts(best_board) == 0:
            return best_board, gen

        # Selection
        def select():
            a, b = random.sample(scored[:20], 2)
            return a[1] if a[0] > b[0] else b[1]

        # Crossover
        new_population = []
        while len(new_population) < pop_size:
            p1, p2 = select(), select()
            cut = random.randint(0, n - 1)
            child = p1[:cut] + p2[cut:]
            # Mutation
            if random.random() < mutation_rate:
                row = random.randrange(n)
                child[row] = random.randrange(n)
            new_population.append(child)
        population = new_population

    return best_board, generations


# Experiment & Comparison


def compare_algorithms(n=5, trials=5):
    results = []

    for algo_name, algo in [
        ("Hill Climbing", hill_climbing),
        ("Simulated Annealing", simulated_annealing),
        ("Genetic Algorithm", genetic_algorithm),
    ]:
        for t in range(trials):
            start = time.time()
            solution, steps = algo(n)
            elapsed = time.time() - start
            conf = conflicts(solution)
            results.append({
                "Algorithm": algo_name,
                "Trial": t + 1,
                "Conflicts": conf,
                "Solved": conf == 0,
                "Steps/Generations": steps,
                "Time (s)": round(elapsed, 4)
            })

    df = pd.DataFrame(results)
    return df


if __name__ == "__main__":
    df = compare_algorithms(n=5, trials=5)
    print(df)
    print("\nSummary:")
    print(df.groupby("Algorithm")[["Solved", "Conflicts", "Time (s)"]].mean())
