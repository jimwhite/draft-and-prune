from z3 import *

# Representative indices
(KIM, MAHR, PARRA, QUINN, STUCKEY, TIAO, UDALL) = range(7)

# Zone variables: zone[i] is the zone (1, 2, or 3) for representative i
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each zone is 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Constraint: Either Parra or Tiao (but not both) in Zone 1
solver.add((zone[PARRA] == 1) != (zone[TIAO] == 1))

# Constraint: Either Tiao or Udall (but not both) in Zone 2
solver.add((zone[TIAO] == 2) != (zone[UDALL] == 2))

# Constraint: Parra and Quinn in the same zone
solver.add(zone[PARRA] == zone[QUINN])

# Constraint: Stuckey and Udall in the same zone
solver.add(zone[STUCKEY] == zone[UDALL])

# Constraint: Zone 3 has more representatives than Zone 2
count_zone1 = Sum([If(zone[i] == 1, 1, 0) for i in range(7)])
count_zone2 = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
count_zone3 = Sum([If(zone[i] == 3, 1, 0) for i in range(7)])
solver.add(count_zone3 > count_zone2)

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
    
    # Add the specific zone assignments from this choice
    for rep, z in assignment.items():
        s_chk.add(zone[rep] == z)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Print the index of the first valid answer (as per typical LSAT format)
print(valid_indices[0] if valid_indices else -1)