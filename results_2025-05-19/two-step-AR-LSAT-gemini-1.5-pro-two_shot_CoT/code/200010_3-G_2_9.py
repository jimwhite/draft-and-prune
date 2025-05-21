from z3 import *

solver = Solver()

selected_works = Array('selected_works', IntSort(), BoolSort())

# Constraint 1: Total Works Selected
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(9)]) >= 5)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(9)]) <= 6)

# Constraint 2: French Works Limit
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(3)]) + Sum([If(selected_works[i], 1, 0) for i in range(6, 8)]) <= 4)

# Constraint 3: Novels Selected
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(6)]) >= 3)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(6)]) <= 4)

# Constraint 4: French Novels vs. Russian Novels
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(3)]) >= Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]))

# Constraint 5: French Plays and Russian Play
solver.add(Implies(And(selected_works[6], selected_works[7]), Not(selected_works[8])))

# Constraint 6: Three French Novels
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(3)]) == 3)

choices = [
    # A: one Russian novel
    [Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]) == 1,
     Sum([If(selected_works[i], 1, 0) for i in range(6,9)]) + Sum([If(selected_works[i], 1, 0) for i in range(3,6)]) == 2],

    # B: two French plays
    [And(selected_works[6], selected_works[7]),
     Sum([If(selected_works[i], 1, 0) for i in range(3,6)]) + Sum([If(selected_works[i], 1, 0) for i in range(6,8)]) == 2],

    # C: one Russian novel, one Russian play
    [Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]) == 1,
     selected_works[8],
     Sum([If(selected_works[i], 1, 0) for i in range(6,8)]) == 0],

    # D: one Russian novel, two French plays
    [Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]) == 1,
     And(selected_works[6], selected_works[7]),
     Not(selected_works[8])],

    # E: two Russian novels, one French play
    [Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]) == 2,
     Sum([If(selected_works[i], 1, 0) for i in range(6, 8)]) == 1,
     Not(selected_works[8])]
]

for i, choice in enumerate(choices):
    solver.push()
    for constraint in choice:
        solver.add(constraint)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
