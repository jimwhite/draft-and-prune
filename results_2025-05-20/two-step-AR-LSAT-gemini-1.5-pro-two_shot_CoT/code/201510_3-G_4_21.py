from z3 import *

# Define variables
season_of_cookbook = Array('season_of_cookbook', IntSort(), IntSort())

# Create solver
solver = Solver()

# Add constraints
i = Int('i')
solver.add(ForAll([i], And(season_of_cookbook[i] >= 0, season_of_cookbook[i] <= 1)))
solver.add(season_of_cookbook[2] != season_of_cookbook[5])
solver.add(season_of_cookbook[0] == season_of_cookbook[3])
solver.add(Implies(season_of_cookbook[0] == 0, season_of_cookbook[4] == 0))
solver.add(Implies(season_of_cookbook[2] == 0, season_of_cookbook[3] == 1))
solver.add(season_of_cookbook[3] == 0)

# Check answer choices
choices = [
    (season_of_cookbook[0] == 1, 'A'),
    (season_of_cookbook[1] == 0, 'B'),
    (season_of_cookbook[2] == 0, 'C'),
    (season_of_cookbook[4] == 1, 'D'),
    (season_of_cookbook[5] == 1, 'E')
]

for constraint, option in choices:
    solver.push()
    solver.add(constraint)
    if solver.check() == sat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()