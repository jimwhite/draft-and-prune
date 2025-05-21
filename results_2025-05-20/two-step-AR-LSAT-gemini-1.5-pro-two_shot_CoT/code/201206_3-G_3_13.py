from z3 import *

# Variables
zone_of_rep = Array('zone_of_rep', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
for i in range(7):
    solver.add(And(zone_of_rep[i] >= 0, zone_of_rep[i] < 3))

solver.add(Xor(zone_of_rep[2] == 0, zone_of_rep[5] == 0))
solver.add(Xor(zone_of_rep[5] == 1, zone_of_rep[6] == 1))
solver.add(zone_of_rep[2] == zone_of_rep[3])
solver.add(zone_of_rep[4] == zone_of_rep[6])

solver.add(Sum([If(zone_of_rep[i] == 2, 1, 0) for i in range(7)]) > Sum([If(zone_of_rep[i] == 1, 1, 0) for i in range(7)]))
solver.add(Sum([If(zone_of_rep[i] == 0, 1, 0) for i in range(7)]) > Sum([If(zone_of_rep[i] == 2, 1, 0) for i in range(7)]))

# Check answer choices
options = [
    (0, 1),  # Kim in Zone 2
    (1, 1),  # Mahr in Zone 2
    (2, 2),  # Parra in Zone 3
    (5, 0),  # Tiao in Zone 1
    (6, 2)   # Udall in Zone 3
]
option_letters = ['A', 'B', 'C', 'D', 'E']

for i, (rep, zone) in enumerate(options):
    solver.push()
    solver.add(zone_of_rep[rep] == zone)
    if solver.check() == sat:
        print(f"Option {option_letters[i]} is correct")
        exit()
    solver.pop()