from z3 import *

# Variables
zone_assignment = Array('zone_assignment', IntSort(), IntSort())
i = Int('i')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([i], And(zone_assignment[i] >= 0, zone_assignment[i] <= 2))) # Constraint 0
solver.add(Xor(zone_assignment[2] == 0, zone_assignment[5] == 0)) # Constraint 1
solver.add(Xor(zone_assignment[5] == 1, zone_assignment[6] == 1)) # Constraint 2
solver.add(zone_assignment[2] == zone_assignment[3]) # Constraint 3
solver.add(zone_assignment[4] == zone_assignment[6]) # Constraint 4
solver.add(Sum([If(zone_assignment[i] == 2, 1, 0) for i in range(7)]) > Sum([If(zone_assignment[i] == 1, 1, 0) for i in range(7)])) # Constraint 5


# Answer choices
choices = [
    [0, 1],  # Kim, Mahr
    [0, 5],  # Kim, Tiao
    [2, 3],  # Parra, Quinn
    [4, 5, 6],  # Stuckey, Tiao, Udall
    [2, 3, 4, 6]  # Parra, Quinn, Stuckey, Udall
]

for choice_index, choice in enumerate(choices):
    solver.push()
    in_zone_3 = [zone_assignment[j] == 2 for j in choice]
    not_in_zone_3 = [zone_assignment[j] != 2 for j in range(7) if j not in choice]
    solver.add(And(*in_zone_3, *not_in_zone_3))
    if solver.check() == sat:
        print(f"Option {chr(65 + choice_index)} is correct")
        exit()
    solver.pop()