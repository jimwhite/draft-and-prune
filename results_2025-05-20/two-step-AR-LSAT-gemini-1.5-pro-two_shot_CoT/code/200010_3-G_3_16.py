from z3 import *

# Variables
slot_of_composition = Array('slot_of_composition', IntSort(), IntSort())
solver = Solver()

# Constraints 0 (Domain)
for i in range(8):
    solver.add(And(slot_of_composition[i] >= 0, slot_of_composition[i] < 8))

# Constraint 1 (Distinctness)
solver.add(Distinct([slot_of_composition[i] for i in range(8)]))

# Constraint 2 (T before F or after R)
solver.add(Or(slot_of_composition[7] + 1 == slot_of_composition[0], slot_of_composition[5] + 1 == slot_of_composition[7]))

# Constraint 3 (Two between F and R)
solver.add(Abs(slot_of_composition[0] - slot_of_composition[5]) > 2)

# Constraint 4 (O first or fifth)
solver.add(Or(slot_of_composition[3] == 0, slot_of_composition[3] == 4))

# Constraint 5 (L or H eighth)
solver.add(Or(slot_of_composition[2] == 7, slot_of_composition[1] == 7))

# Constraint 6 (P before S)
solver.add(slot_of_composition[4] < slot_of_composition[6])

# Constraint 7 (One between O and S)
solver.add(Abs(slot_of_composition[3] - slot_of_composition[6]) > 1)

# Constraint 8 (S is fourth)
solver.add(slot_of_composition[6] == 3)

# Mapping
mapping = {'F': 0, 'H': 1, 'L': 2, 'O': 3, 'P': 4, 'R': 5, 'S': 6, 'T': 7}

# Answer choices
choices = [
    ["F", "H", "P"],
    ["H", "P", "L"],
    ["O", "P", "R"],
    ["O", "P", "T"],
    ["P", "R", "T"]
]

# Check each choice
for i, choice in enumerate(choices):
    solver.push()
    solver.add(slot_of_composition[mapping[choice[0]]] == 0)
    solver.add(slot_of_composition[mapping[choice[1]]] == 1)
    solver.add(slot_of_composition[mapping[choice[2]]] == 2)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()