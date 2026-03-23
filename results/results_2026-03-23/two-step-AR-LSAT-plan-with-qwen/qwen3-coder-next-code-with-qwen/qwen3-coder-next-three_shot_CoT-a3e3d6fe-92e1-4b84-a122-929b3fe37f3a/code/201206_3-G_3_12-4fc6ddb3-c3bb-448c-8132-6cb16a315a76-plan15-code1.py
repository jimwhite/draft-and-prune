from z3 import *

# Representative indices
(KIM, MAHR, PARRA, QUINN, STUCKEY, TIAO, UDALL) = range(7)

# Zone variables: zone[i] is the zone (1, 2, or 3) for representative i
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each representative is assigned to zone 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Parra-or-Tiao constraint: Exactly one of Parra or Tiao is in Zone 1
solver.add(Or(
    And(zone[PARRA] == 1, zone[TIAO] != 1),
    And(zone[TIAO] == 1, zone[PARRA] != 1)
))

# Tiao-or-Udall constraint: Exactly one of Tiao or Udall is in Zone 2
solver.add(Or(
    And(zone[TIAO] == 2, zone[UDALL] != 2),
    And(zone[UDALL] == 2, zone[TIAO] != 2)
))

# Parra-Quinn constraint: Parra and Quinn in same zone
solver.add(zone[PARRA] == zone[QUINN])

# Stuckey-Udall constraint: Stuckey and Udall in same zone
solver.add(zone[STUCKEY] == zone[UDALL])

# Zone-count constraint: Zone 3 has more representatives than Zone 2
zone_count = lambda z: Sum([If(zone[i] == z, 1, 0) for i in range(7)])
solver.add(zone_count(3) > zone_count(2))

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
    
    # Add the specific assignment constraints
    for rep, z in assignment.items():
        s_chk.add(zone[rep] == z)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)