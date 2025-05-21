from z3 import *

# Define variables
zone_assignment = Array('zone_assignment', IntSort(), IntSort())
i = Int('i')

# Create solver and add base constraints
solver = Solver()
solver.add(ForAll([i], And(zone_assignment[i] >= 0, zone_assignment[i] <= 2)))
solver.add(Xor(zone_assignment[2] == 0, zone_assignment[5] == 0))
solver.add(Xor(zone_assignment[5] == 1, zone_assignment[6] == 1))
solver.add(zone_assignment[2] == zone_assignment[3])
solver.add(zone_assignment[4] == zone_assignment[6])
solver.add(Sum([If(zone_assignment[i] == 2, 1, 0) for i in range(7)]) > Sum([If(zone_assignment[i] == 1, 1, 0) for i in range(7)]))

# Answer choices
options = [
    [[0, 2], [4, 6], [1, 3, 5]],  # A
    [[0, 5], [4, 6], [1, 2, 3]],  # B
    [[2, 3], [0, 6], [1, 4, 5]],  # C
    [[4, 6], [0, 5], [1, 2, 3]],  # D
    [[5], [0, 2, 3], [4, 6]]     # E
]

# Check each option
for option_index, option in enumerate(options):
    solver.push()
    for zone_index, reps in enumerate(option):
        for rep in reps:
            solver.add(zone_assignment[rep] == zone_index)
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()