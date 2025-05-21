from z3 import *

# Variables
pos = Array('pos', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
h = Int('h')
solver.add(ForAll([h], And(pos[h] >= 0, pos[h] <= 6)))  # Domain
solver.add(Distinct([pos[h] for h in range(7)]))  # Distinctness
solver.add(Or(pos[0] == 5, pos[0] == 6))  # J in Evening
solver.add(And(pos[1] != 0, pos[1] != 1))  # K not in Morning
solver.add(And(pos[1] < pos[2], pos[2] < pos[3]))  # L after K and before M

# Answer choices
options = [
    pos[1] > pos[0],  # A: K after J
    pos[2] > pos[0],  # B: L after J
    pos[6] > pos[0],  # C: P after J
    And(pos[4] > pos[3], pos[5] > pos[3]),  # D: N and O after M
    And(pos[4] > pos[1], pos[6] > pos[1])   # E: N and P after K
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()