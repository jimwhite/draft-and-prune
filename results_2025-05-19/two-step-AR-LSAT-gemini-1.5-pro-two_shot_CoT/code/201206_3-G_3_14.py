from z3 import *

# Variables
zone_assignment = Array('zone_assignment', IntSort(), IntSort())
solver = Solver()

# Constraints
for i in range(7):
    solver.add(And(zone_assignment[i] >= 0, zone_assignment[i] < 3))

for i in range(7):
    solver.add(Or(zone_assignment[i] == 0, zone_assignment[i] == 1, zone_assignment[i] == 2))

solver.add(Xor(zone_assignment[2] == 0, zone_assignment[5] == 0))
solver.add(Xor(zone_assignment[5] == 1, zone_assignment[6] == 1))
solver.add(zone_assignment[2] == zone_assignment[3])
solver.add(zone_assignment[4] == zone_assignment[6])
solver.add(Sum([If(zone_assignment[i] == 2, 1, 0) for i in range(7)]) > Sum([If(zone_assignment[i] == 1, 1, 0) for i in range(7)]))

# Answer choices
choices = [
    And(zone_assignment[0] == 0, zone_assignment[4] == 0),
    And(zone_assignment[0] == 2, zone_assignment[4] == 2),
    And(zone_assignment[1] == 2, zone_assignment[4] == 2),
    And(zone_assignment[1] == 2, zone_assignment[6] == 2),
    And(zone_assignment[2] == 0, zone_assignment[4] == 0)
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()