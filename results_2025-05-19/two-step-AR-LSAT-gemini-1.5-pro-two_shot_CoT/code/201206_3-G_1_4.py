from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())
i = Int('i')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([i], And(schedule[i] >= 0, schedule[i] <= 5))) # Constraint 0
solver.add(Distinct([schedule[i] for i in range(6)])) # Constraint 1

# Constraint 2
solver.add(Or(
    And(schedule[0] == 1, schedule[1] == 5),
    And(schedule[0] == 5, schedule[1] == 1),
    And(schedule[2] == 1, schedule[3] == 5),
    And(schedule[2] == 5, schedule[3] == 1),
    And(schedule[4] == 1, schedule[5] == 5),
    And(schedule[4] == 5, schedule[5] == 1)
))

# Constraint 3
solver.add(And(
    Implies(Or(schedule[0] == 2, schedule[1] == 2), Not(Or(schedule[2] == 4, schedule[3] == 4, schedule[4] == 4, schedule[5] == 4))),
    Implies(Or(schedule[2] == 2, schedule[3] == 2), Not(Or(schedule[0] == 4, schedule[1] == 4, schedule[4] == 4, schedule[5] == 4))),
    Implies(Or(schedule[4] == 2, schedule[5] == 2), Not(Or(schedule[0] == 4, schedule[1] == 4, schedule[2] == 4, schedule[3] == 4)))
))

solver.add(Or(schedule[1] == 3, schedule[3] == 3, schedule[5] == 3)) # Constraint 4

# Constraint 5
solver.add(And(
    Implies(Or(schedule[0] == 0, schedule[1] == 0), Or(schedule[2] == 4, schedule[3] == 4, schedule[4] == 4, schedule[5] == 4)),
    Implies(Or(schedule[2] == 0, schedule[3] == 0), Or(schedule[4] == 4, schedule[5] == 4))
))

solver.add(Or(schedule[0] == 0, schedule[2] == 0, schedule[4] == 0)) # Constraint 6
solver.add(Or(schedule[0] == 1, schedule[2] == 1, schedule[4] == 1)) # Constraint 7

# Answer choices
options = [
    (0, 2),  # Lan's session meets Wednesday morning.
    (3, 2),  # Lan's session meets Thursday afternoon.
    (5, 3),  # Nessa's session meets Friday afternoon.
    (2, 4),  # Olivia's session meets Thursday morning.
    (4, 4)   # Olivia's session meets Friday morning.
]

option_labels = ['A', 'B', 'C', 'D', 'E']

for i, (slot, assistant) in enumerate(options):
    solver.push()
    solver.add(schedule[slot] == assistant)
    if solver.check() == unsat:
        print(f"Option {option_labels[i]} is correct")
        exit()
    solver.pop()