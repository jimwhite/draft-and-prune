from z3 import *

# Variables
target_days = Array('target_days', IntSort(), IntSort())
i = Int('i')
c = Int('c')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([i], And(target_days[i] >= 1, target_days[i] <= 3)))
solver.add(ForAll([c], target_days[c * 2 + 0] <= target_days[c * 2 + 1]))
solver.add(And(target_days[0 * 2 + 1] < target_days[1 * 2 + 1], target_days[0 * 2 + 1] < target_days[2 * 2 + 1]))
solver.add(target_days[1 * 2 + 0] < target_days[2 * 2 + 0])
solver.add(target_days[2 * 2 + 0] < target_days[2 * 2 + 1])

# Answer choices
options = [
    target_days[0 * 2 + 1] != 2,  # A
    target_days[0 * 2 + 0] != 2,  # B
    target_days[0 * 2 + 0] != 1,  # C
    target_days[1 * 2 + 0] != 2,  # D
    target_days[1 * 2 + 0] != 1   # E
]

for idx, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == unsat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()