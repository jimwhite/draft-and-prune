from z3 import *

# Variables
zone_assignment = Array('zone_assignment', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
for i in range(7):
    solver.add(And(zone_assignment[i] >= 0, zone_assignment[i] <= 2))

for i in range(7):
    for j in range(7):
        if i < j:
            solver.add(Implies(i != j, zone_assignment[i] != zone_assignment[j]))

solver.add(Xor(zone_assignment[2] == 0, zone_assignment[5] == 0))
solver.add(Xor(zone_assignment[5] == 1, zone_assignment[6] == 1))
solver.add(zone_assignment[2] == zone_assignment[3])
solver.add(zone_assignment[4] == zone_assignment[6])

solver.add(Sum([If(zone_assignment[i] == 2, 1, 0) for i in range(7)]) > Sum([If(zone_assignment[i] == 1, 1, 0) for i in range(7)]))

# Answer choices
choices = [
    [0, 1],
    [0, 5],
    [2, 3],
    [4, 5, 6],
    [2, 3, 4, 6]
]

for choice_index, choice in enumerate(choices):
    solver.push()
    for rep in choice:
        solver.add(zone_assignment[rep] == 2)
    for rep in range(7):
        if rep not in choice:
            solver.add(zone_assignment[rep] != 2)

    if solver.check() == sat:
        print(f"Option {chr(65 + choice_index)} is correct")
        exit()
    solver.pop()