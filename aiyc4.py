import random
import time
import pandas as pd
from simpleai.search import SearchProblem
from simpleai.search.local import hill_climbing, simulated_annealing, genetic


class NQueensProblem(SearchProblem):
    def __init__(self, n):
        self.n = n
        initial = tuple(random.randrange(n) for _ in range(n))
        super().__init__(initial_state=initial)

    def actions(self, state):
        actions = []
        for row in range(self.n):
            for col in range(self.n):
                if col != state[row]:
                    actions.append((row, col))
        return actions

    def result(self, state, action):
        row, col = action
        new_state = list(state)
        new_state[row] = col
        return tuple(new_state)

    def value(self, state):
        # Maximize negative conflicts
        return -self.conflicts(state)

    def conflicts(self, state):
        n = self.n
        count = 0
        for r1 in range(n):
            for r2 in range(r1 + 1, n):
                c1, c2 = state[r1], state[r2]
                if c1 == c2 or abs(c1 - c2) == abs(r1 - r2):
                    count += 1
        return count

    def generate_random_state(self):
        """Required for genetic algorithm in simpleai"""
        return tuple(random.randrange(self.n) for _ in range(self.n))

    def crossover(self, state1, state2):
        """Single-point crossover between two boards"""
        cut = random.randint(0, self.n - 1)
        child = state1[:cut] + state2[cut:]
        return tuple(child)

    def mutate(self, state):
        """Mutate by moving one queen to a random column"""
        row = random.randrange(self.n)
        col = random.randrange(self.n)
        new_state = list(state)
        new_state[row] = col
        return tuple(new_state)


# Wrappers
def hill_climbing_ai(n=5, max_steps=1000):
    problem = NQueensProblem(n)
    result = hill_climbing(problem, iterations_limit=max_steps)
    return list(result.state)


def simulated_annealing_ai(n=5, max_steps=1000):
    problem = NQueensProblem(n)
    result = simulated_annealing(problem, iterations_limit=max_steps)
    return list(result.state)


def genetic_ai(n=5, pop_size=50, generations=500, mutation_rate=0.2):
    problem = NQueensProblem(n)
    result = genetic(
        problem,
        iterations_limit=generations,
        population_size=pop_size,
        mutation_chance=mutation_rate
    )
    return list(result.state)


# Experiment & Comparison
def compare_algorithms(n=5, trials=5):
    results = []

    for algo_name, algo in [
        ("Hill Climbing", hill_climbing_ai),
        ("Simulated Annealing", simulated_annealing_ai),
        ("Genetic Algorithm", genetic_ai),
    ]:
        for t in range(trials):
            start = time.time()
            solution = algo(n)
            elapsed = time.time() - start

            problem = NQueensProblem(n)
            conf = problem.conflicts(solution)

            results.append({
                "Algorithm": algo_name,
                "Trial": t + 1,
                "Conflicts": conf,
                "Solved": conf == 0,
                "Time (s)": round(elapsed, 4)
            })

    df = pd.DataFrame(results)
    return df


if __name__ == "__main__":
    df = compare_algorithms(n=5, trials=100)
    print(df)
    print("\nSummary:")
    print(df.groupby("Algorithm")[["Solved", "Conflicts", "Time (s)"]].mean())
