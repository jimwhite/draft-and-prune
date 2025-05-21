from z3 import *

# Variables
season_of_cookbook = Array('season_of_cookbook', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
for i in range(6):
    solver.add(And(season_of_cookbook[i] >= 0, season_of_cookbook[i] <= 1))
solver.add(season_of_cookbook[2] != season_of_cookbook[5])
solver.add(season_of_cookbook[0] == season_of_cookbook[3])
solver.add(Implies(season_of_cookbook[0] == 0, season_of_cookbook[4] == 0))
solver.add(Implies(season_of_cookbook[2] == 0, season_of_cookbook[3] == 1))
solver.add(season_of_cookbook[2] == 0)

# Answer choices
answer_choices = [
    [0, 4],  # K and O
    [1, 3],  # L and N
    [1, 4],  # L and O
    [3, 5],  # N and P
    [4, 5]   # O and P
]

# Check each answer choice
for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(season_of_cookbook[choice[0]] == 0)
    solver.add(season_of_cookbook[choice[1]] == 0)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()