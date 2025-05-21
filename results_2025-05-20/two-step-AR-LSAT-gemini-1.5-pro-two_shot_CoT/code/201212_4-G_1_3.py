from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 0, i < 7), And(schedule[i] >= 0, schedule[i] < 7))))

# Constraint 1 (Distinctness)
solver.add(Distinct([schedule[i] for i in range(7)]))

# Constraint 2 (J in Evening)
solver.add(Or(schedule[5] == 0, schedule[6] == 0))

# Constraint 3 (K not in Morning)
solver.add(And(schedule[0] != 1, schedule[1] != 1))

# Constraint 4 (K before L before M)
i = Int('i')
j = Int('j')
k = Int('k')
solver.add(ForAll([i, j, k], Implies(And(schedule[i] == 1, schedule[j] == 2, schedule[k] == 3), And(i < j, j < k))))


# Check answer choices
options = [
    And(schedule[5] != 1, schedule[6] != 1),  # A: K is NOT shown in the evening
    And(schedule[2] != 2, schedule[3] != 2, schedule[4] != 2),  # B: L is NOT shown in the afternoon
    And(schedule[5] != 2, schedule[6] != 2),  # C: L is NOT shown in the evening
    And(schedule[0] != 3, schedule[1] != 3),  # D: M is NOT shown in the morning
    And(schedule[2] != 3, schedule[3] != 3, schedule[4] != 3)   # E: M is NOT shown in the afternoon
]

for idx, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == unsat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()