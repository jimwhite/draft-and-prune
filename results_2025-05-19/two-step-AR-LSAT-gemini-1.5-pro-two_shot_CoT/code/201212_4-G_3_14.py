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
solver.add(target_days[1 * 2 + 1] < target_days[2 * 2 + 0])

# Answer choices
choices = [
    target_days[0 * 2 + 0] == 2,  # Image Website
    target_days[0 * 2 + 1] == 2,  # Image Voicemail
    target_days[1 * 2 + 0] == 2,  # Solide Website
    target_days[2 * 2 + 1] == 2,  # Truvest Voicemail
    target_days[2 * 2 + 0] == 2   # Truvest Website
]

for idx, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()