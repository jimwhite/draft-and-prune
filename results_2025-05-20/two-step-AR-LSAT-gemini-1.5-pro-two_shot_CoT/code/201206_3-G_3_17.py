from z3 import *

# Define variables
zone_assignment = Array('zone_assignment', IntSort(), IntSort())
solver = Solver()

# Constraint 1: Domain
i = Int('i')
solver.add(ForAll([i], And(zone_assignment[i] >= 0, zone_assignment[i] < 3)))

# Constraint 2: Parra/Tiao Zone 1
solver.add(Xor(zone_assignment[2] == 0, zone_assignment[5] == 0))

# Constraint 3: Tiao/Udall Zone 2
solver.add(Xor(zone_assignment[5] == 1, zone_assignment[6] == 1))

# Constraint 4: Parra/Quinn Same Zone
solver.add(zone_assignment[2] == zone_assignment[3])

# Constraint 5: Stuckey/Udall Same Zone
solver.add(zone_assignment[4] == zone_assignment[6])

# Constraint 6: Zone 3 > Zone 2
solver.add(Sum([If(zone_assignment[i] == 2, 1, 0) for i in range(7)]) > Sum([If(zone_assignment[i] == 1, 1, 0) for i in range(7)]))

# Question Premise: Mahr and Stuckey in the same zone
solver.add(zone_assignment[1] == zone_assignment[4])

# Check answer choices
answer_choices = [
    zone_assignment[0] == 1,  # A: Kim works in Zone 2
    zone_assignment[1] == 0,  # B: Mahr works in Zone 1
    zone_assignment[2] == 2,  # C: Parra works in Zone 3
    zone_assignment[4] == 1,  # D: Stuckey works in Zone 2
    zone_assignment[5] == 0   # E: Tiao works in Zone 1
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()