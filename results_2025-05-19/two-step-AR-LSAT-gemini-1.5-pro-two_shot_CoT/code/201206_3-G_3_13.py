from z3 import *

# Variables
zone_assignment = Array('zone_assignment', IntSort(), IntSort())
i = Int('i')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([i], And(zone_assignment[i] >= 0, zone_assignment[i] < 3))) # Constraint 0
solver.add(ForAll([i], Or(zone_assignment[i] == 0, zone_assignment[i] == 1, zone_assignment[i] == 2))) # Constraint 1

solver.add(Xor(zone_assignment[2] == 0, zone_assignment[5] == 0)) # Constraint 2
solver.add(Xor(zone_assignment[5] == 1, zone_assignment[6] == 1)) # Constraint 3
solver.add(zone_assignment[2] == zone_assignment[3]) # Constraint 4
solver.add(zone_assignment[4] == zone_assignment[6]) # Constraint 5

solver.add(Sum([If(zone_assignment[i] == 2, 1, 0) for i in range(7)]) > Sum([If(zone_assignment[i] == 1, 1, 0) for i in range(7)])) # Constraint 6
solver.add(Sum([If(zone_assignment[i] == 0, 1, 0) for i in range(7)]) > Sum([If(zone_assignment[i] == 2, 1, 0) for i in range(7)])) # Constraint 7


# Answer choices
answer_choices = [
    (1, 1),  # Kim works in Zone 2
    (1, 1),  # Mahr works in Zone 2.
    (2, 2),  # Parra works in Zone 3.
    (5, 0),  # Tiao works in Zone 1.
    (6, 2)   # Udall works in Zone 3.
]

for idx, (rep, zone) in enumerate(answer_choices):
    solver.push()
    solver.add(zone_assignment[rep] == zone)
    if solver.check() == sat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()