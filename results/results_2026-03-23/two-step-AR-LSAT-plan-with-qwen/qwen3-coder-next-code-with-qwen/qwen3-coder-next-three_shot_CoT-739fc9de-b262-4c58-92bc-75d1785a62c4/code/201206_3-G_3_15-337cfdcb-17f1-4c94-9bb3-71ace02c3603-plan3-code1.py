from z3 import *

# Representative indices
(KIM, MAHR, PARRA, QUINN, STUCKEY, TIAO, UDALL) = range(7)

# Zone variables: zone[i] = zone assignment for representative i (1, 2, or 3)
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each representative assigned to zone 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Mutual exclusion for Zone 1: either Parra or Tiao (but not both)
solver.add(Xor(zone[PARRA] == 1, zone[TIAO] == 1))

# Mutual exclusion for Zone 2: either Tiao or Udall (but not both)
solver.add(Xor(zone[TIAO] == 2, zone[UDALL] == 2))

# Grouping constraints: Parra and Quinn in same zone
solver.add(zone[PARRA] == zone[QUINN])

# Grouping constraints: Stuckey and Udall in same zone
solver.add(zone[STUCKEY] == zone[UDALL])

# Zone size constraint: count(Zone 3) > count(Zone 2)
count_zone = lambda z: Sum([If(zone[i] == z, 1, 0) for i in range(7)])
solver.add(count_zone(3) > count_zone(2))

# Answer choices
answer_choices = [
    ['Kim', 'Mahr'],                    # Choice 0: Kim and Mahr in Zone 3
    ['Kim', 'Tiao'],                   # Choice 1: Kim and Tiao in Zone 3
    ['Parra', 'Quinn'],                # Choice 2: Parra and Quinn in Zone 3
    ['Stuckey', 'Tiao', 'Udall'],      # Choice 3: Stuckey, Tiao, Udall in Zone 3
    ['Parra', 'Quinn', 'Stuckey', 'Udall']  # Choice 4: Parra, Quinn, Stuckey, Udall in Zone 3
]

# Map names to indices for easier reference
name_to_idx = {
    'Kim': KIM, 'Mahr': MAHR, 'Parra': PARRA,
    'Quinn': QUINN, 'Stuckey': STUCKEY, 'Tiao': TIAO, 'Udall': UDALL
}

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Get set of representatives claimed to be in Zone 3
    zone3_set = {name_to_idx[name] for name in choice}
    
    # Assert that representatives in the choice are in Zone 3
    for rep_idx in zone3_set:
        s_chk.add(zone[rep_idx] == 3)
    
    # Assert that representatives NOT in the choice are NOT in Zone 3
    for rep_idx in range(7):
        if rep_idx not in zone3_set:
            s_chk.add(zone[rep_idx] != 3)
    
    # Check satisfiability
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Output the index of the first (lowest) valid choice
if answer_index_list:
    print(answer_index_list[0])
else:
    print(-1)