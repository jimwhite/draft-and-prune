from z3 import *

# Variables
slot_of_composition = Array('slot_of_composition', IntSort(), IntSort())
c = Int('c')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([c], And(slot_of_composition[c] >= 0, slot_of_composition[c] <= 7))) # Constraint 0
solver.add(Distinct([slot_of_composition[c] for c in range(8)])) # Constraint 1
solver.add(Or(slot_of_composition[7] + 1 == slot_of_composition[0], slot_of_composition[7] - 1 == slot_of_composition[5])) # Constraint 2
solver.add(Or(slot_of_composition[5] - slot_of_composition[0] > 2, slot_of_composition[0] - slot_of_composition[5] > 2)) # Constraint 3
solver.add(Or(slot_of_composition[3] == 0, slot_of_composition[3] == 4)) # Constraint 4
solver.add(Or(slot_of_composition[2] == 7, slot_of_composition[1] == 7)) # Constraint 5
solver.add(slot_of_composition[4] < slot_of_composition[6]) # Constraint 6
solver.add(Or(slot_of_composition[6] - slot_of_composition[3] > 1, slot_of_composition[3] - slot_of_composition[6] > 1)) # Constraint 7
solver.add(slot_of_composition[3] == slot_of_composition[7] + 1) # Constraint 8

# Answer choices
answer_choices = [
    (0, 1),  # "first or second"
    (1, 2),  # "second or third"
    (3, 5),  # "fourth or sixth"
    (3, 6),  # "fourth or seventh"
    (5, 6)   # "sixth or seventh"
]

for i, (a, b) in enumerate(answer_choices):
    solver.push()
    solver.add(Or(slot_of_composition[0] == a, slot_of_composition[0] == b))
    if solver.check() == sat:
        solver.push()
        solver.add(Not(Or(slot_of_composition[0] == a, slot_of_composition[0] == b)))
        if solver.check() == unsat:
            print(f"Option {chr(65 + i)} is correct")
            exit()
        solver.pop()
    solver.pop()