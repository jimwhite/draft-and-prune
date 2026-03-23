from z3 import *

# Representative indices
(KIM, MAHR, PARRA, QUINN, STUCKEY, TIAO, UDALL) = range(7)

# Zone variables: zone[i] = zone assigned to representative i (1, 2, or 3)
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Zone assignment constraints: each person assigned to zone 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Either Parra or Tiao (but not both) in Zone 1
solver.add(Xor(zone[PARRA] == 1, zone[TIAO] == 1))

# Either Tiao or Udall (but not both) in Zone 2
solver.add(Xor(zone[TIAO] == 2, zone[UDALL] == 2))

# Parra and Quinn in same zone
solver.add(zone[PARRA] == zone[QUINN])

# Stuckey and Udall in same zone
solver.add(zone[STUCKEY] == zone[UDALL])

# Zone 3 has more people than Zone 2
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
feasible_indices = []
for idx, assignment in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific zone assignments from this answer choice
    for person, z in assignment.items():
        s_chk.add(zone[person] == z)
    
    if s_chk.check() == sat:
        feasible_indices.append(idx)

# Output the index of the first feasible answer choice (as per question format)
print(feasible_indices[0] if feasible_indices else -1)