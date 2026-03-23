from z3 import *

# Representative indices
(KIM, MAHR, PARRA, QUINN, STUCKEY, TIAO, UDALL) = range(7)

# Zone variables for each representative
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each representative assigned to zone 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Exactly-one constraints for Zone 1: either Parra or Tiao (but not both)
solver.add(Or(
    And(zone[PARRA] == 1, zone[TIAO] != 1),
    And(zone[TIAO] == 1, zone[PARRA] != 1)
))

# Exactly-one constraints for Zone 2: either Tiao or Udall (but not both)
solver.add(Or(
    And(zone[TIAO] == 2, zone[UDALL] != 2),
    And(zone[UDALL] == 2, zone[TIAO] != 2)
))

# Equivalence constraints: Parra and Quinn in same zone
solver.add(zone[PARRA] == zone[QUINN])

# Equivalence constraints: Stuckey and Udall in same zone
solver.add(zone[STUCKEY] == zone[UDALL])

# Zone size constraint: more representatives in Zone 3 than Zone 2
count_zone = lambda z: Sum([If(zone[i] == z, 1, 0) for i in range(7)])
solver.add(count_zone(3) > count_zone(2))

# Answer choices
answer_choices = [
    # Zone 1: Kim, Parra; Zone 2: Stuckey, Udall; Zone 3: Mahr, Quinn, Tiao
    {KIM: 1, PARRA: 1, STUCKEY: 2, UDALL: 2, MAHR: 3, QUINN: 3, TIAO: 3},
    # Zone 1: Kim, Tiao; Zone 2: Stuckey, Udall; Zone 3: Mahr, Parra, Quinn
    {KIM: 1, TIAO: 1, STUCKEY: 2, UDALL: 2, MAHR: 3, PARRA: 3, QUINN: 3},
    # Zone 1: Parra, Quinn; Zone 2: Kim, Udall; Zone 3: Mahr, Stuckey, Tiao
    {PARRA: 1, QUINN: 1, KIM: 2, UDALL: 2, MAHR: 3, STUCKEY: 3, TIAO: 3},
    # Zone 1: Stuckey, Udall; Zone 2: Kim, Tiao; Zone 3: Mahr, Parra, Quinn
    {STUCKEY: 1, UDALL: 1, KIM: 2, TIAO: 2, MAHR: 3, PARRA: 3, QUINN: 3},
    # Zone 1: Tiao; Zone 2: Kim, Parra, Quinn; Zone 3: Stuckey, Udall
    {TIAO: 1, KIM: 2, PARRA: 2, QUINN: 2, STUCKEY: 3, UDALL: 3}
]

# Check each answer choice
valid_indices = []
for idx, assignment in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add assignment constraints
    for rep, z in assignment.items():
        s_chk.add(zone[rep] == z)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)