from z3 import *

# Representative indices
(KIM, MAHR, PARRA, QUINN, STUCKEY, TIAO, UDALL) = range(7)

# Zone variables: zone[i] is the zone (1, 2, or 3) for representative i
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each zone is 1, 2, or 3
for i in range(7):
    solver.add(zone[i] >= 1, zone[i] <= 3)

# Parra/Tiao Zone 1 constraint: exactly one of them is in Zone 1
solver.add(Xor(zone[PARRA] == 1, zone[TIAO] == 1))

# Tiao/Udall Zone 2 constraint: exactly one of them is in Zone 2
solver.add(Xor(zone[TIAO] == 2, zone[UDALL] == 2))

# Parra and Quinn same zone
solver.add(zone[PARRA] == zone[QUINN])

# Stuckey and Udall same zone
solver.add(zone[STUCKEY] == zone[UDALL])

# Zone 3 size > Zone 2 size
cnt3 = Sum([If(zone[i] == 3, 1, 0) for i in range(7)])
cnt2 = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
solver.add(cnt3 > cnt2)

# Answer choices
answer_choices = [
    # Choice 0: 'Zone 1: Kim, Parra Zone 2: Stuckey, Udall Zone 3: Mahr, Quinn, Tiao'
    {KIM: 1, PARRA: 1, STUCKEY: 2, UDALL: 2, MAHR: 3, QUINN: 1, TIAO: 3},
    # Choice 1: 'Zone 1: Kim, Tiao Zone 2: Stuckey, Udall Zone 3: Mahr, Parra, Quinn'
    {KIM: 1, TIAO: 1, STUCKEY: 2, UDALL: 2, MAHR: 3, PARRA: 3, QUINN: 3},
    # Choice 2: 'Zone 1: Parra, Quinn Zone 2: Kim, Udall Zone 3: Mahr, Stuckey, Tiao'
    {PARRA: 1, QUINN: 1, KIM: 2, UDALL: 2, MAHR: 3, STUCKEY: 3, TIAO: 3},
    # Choice 3: 'Zone 1: Stuckey, Udall Zone 2: Kim, Tiao Zone 3: Mahr, Parra, Quinn'
    {STUCKEY: 1, UDALL: 1, KIM: 2, TIAO: 2, MAHR: 3, PARRA: 3, QUINN: 3},
    # Choice 4: 'Zone 1: Tiao Zone 2: Kim, Parra, Quinn Zone 3: Stuckey, Udall'
    {TIAO: 1, KIM: 2, PARRA: 2, QUINN: 2, STUCKEY: 3, UDALL: 3}
]

# Check each answer choice
answer_index_list = []
for idx, assignment in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific zone assignments for this choice
    for rep, z in assignment.items():
        s_chk.add(zone[rep] == z)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Print the index of the correct choice (only one should be SAT)
print(answer_index_list[0] if answer_index_list else -1)