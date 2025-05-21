from z3 import *

# Variables
cookbook_season = Array('cookbook_season', IntSort(), IntSort())
solver = Solver()

# Constraints
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i <= 5), And(cookbook_season[i] >= 0, cookbook_season[i] <= 1))))
solver.add(cookbook_season[2] != cookbook_season[5])
solver.add(cookbook_season[0] == cookbook_season[3])
solver.add(Implies(cookbook_season[0] == 0, cookbook_season[4] == 0))
solver.add(Implies(cookbook_season[2] == 0, cookbook_season[3] == 1))

# Question Constraint: N is published in the fall
solver.add(cookbook_season[3] == 0)

# Answer Choices
options = [
    (0, 1),  # A: K is published in the spring
    (1, 0),  # B: L is published in the fall
    (2, 0),  # C: M is published in the fall
    (4, 1),  # D: O is published in the spring
    (5, 1)   # E: P is published in the spring
]

for option_index, (cookbook_id, season_id) in enumerate(options):
    solver.push()
    solver.add(cookbook_season[cookbook_id] == season_id)
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()