from z3 import *

solver = Solver()

selected_works = Array('selected_works', IntSort(), BoolSort())

# Constraint 1: At least five and at most six works
solver.add(And(5 <= Sum([If(selected_works[i], 1, 0) for i in range(9)]), Sum([If(selected_works[i], 1, 0) for i in range(9)]) <= 6))

# Constraint 2: No more than four French works
solver.add(Sum([If(selected_works[i], 1, 0) for i in [0, 1, 2, 6, 7]]) <= 4)

# Constraint 3: At least three but no more than four novels
solver.add(And(3 <= Sum([If(selected_works[i], 1, 0) for i in range(6)]), Sum([If(selected_works[i], 1, 0) for i in range(6)]) <= 4))

# Constraint 4: At least as many French novels as Russian novels
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(3)]) >= Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]))

# Constraint 5: If both French plays are selected, then the Russian play is not selected
solver.add(Implies(And(selected_works[6], selected_works[7]), Not(selected_works[8])))

choices = [
    [0, 3, 4, 6, 8],  # A
    [0, 1, 3, 6, 7, 8],  # B
    [0, 1, 3, 4, 6, 7],  # C
    [0, 1, 2, 3, 6, 7],  # D
    [0, 1, 2, 3, 4, 8]   # E
]

for i, choice in enumerate(choices):
    solver.push()
    for j in range(9):
        if j in choice:
            solver.add(selected_works[j] == True)
        else:
            solver.add(selected_works[j] == False)

    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
