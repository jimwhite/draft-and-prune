from z3 import *

# Variables
selected_works = Array('selected_works', IntSort(), BoolSort())
solver = Solver()

# Constraint 1: At least five and at most six works
solver.add(5 <= Sum([If(selected_works[i], 1, 0) for i in range(9)]) <= 6)

# Constraint 2: No more than four French works
solver.add(Sum([If(selected_works[i], 1, 0) for i in [0, 1, 2, 6, 7]]) <= 4)

# Constraint 3: At least three but no more than four novels
solver.add(3 <= Sum([If(selected_works[i], 1, 0) for i in range(6)]) <= 4)

# Constraint 4: At least as many French novels as Russian novels
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(3)]) >= Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]))

# Constraint 5: If both French plays are selected, then the Russian play is not selected
solver.add(Implies(And(selected_works[6], selected_works[7]), Not(selected_works[8])))

# Answer choices
choices = [
    ([1, 0, 0, 0, 1, 1, 0, 1, 1], 'A'),
    ([0, 1, 1, 1, 0, 0, 1, 1, 1], 'B'),
    ([0, 1, 1, 0, 1, 1, 1, 1, 0], 'C'),
    ([1, 1, 1, 1, 0, 0, 1, 1, 0], 'D'),
    ([1, 1, 1, 0, 1, 1, 0, 0, 1], 'E')
]

for counts, option in choices:
    solver.push()  # Push the current solver state
    for i in range(9):
        solver.add(selected_works[i] == bool(counts[i]))
    if solver.check() == sat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()  # Backtrack to the previous state

