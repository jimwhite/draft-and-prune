from z3 import *

# Representative indices: Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall
(KIM, MAHR, PARRA, QUINN, STUCKEY, TIAO, UDALL) = range(7)

# Zone variables: zone[i] is the zone (1, 2, or 3) for representative i
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each representative is assigned to zone 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Parra/Tiao Zone 1 constraint: exactly one of them is in Zone 1
solver.add(Xor(zone[PARRA] == 1, zone[TIAO] == 1))

# Tiao/Udall Zone 2 constraint: exactly one of them is in Zone 2
solver.add(Xor(zone[TIAO] == 2, zone[UDALL] == 2))

# Parra/Quinn same zone constraint
solver.add(zone[PARRA] == zone[QUINN])

# Stuckey/Udall same zone constraint
solver.add(zone[STUCKEY] == zone[UDALL])

# Zone 3 > Zone 2 size constraint
count_zone2 = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
count_zone3 = Sum([If(zone[i] == 3, 1, 0) for i in range(7)])
solver.add(count_zone3 > count_zone2)

# Answer choices
answer_choices = [
    ['Kim', 'Mahr'],                    # Index 0: Kim and Mahr in Zone 3
    ['Kim', 'Tiao'],                   # Index 1: Kim and Tiao in Zone 3
    ['Parra', 'Quinn'],                # Index 2: Parra and Quinn in Zone 3
    ['Stuckey', 'Tiao', 'Udall'],     # Index 3: Stuckey, Tiao, Udall in Zone 3
    ['Parra', 'Quinn', 'Stuckey', 'Udall']  # Index 4: Parra, Quinn, Stuckey, Udall in Zone 3
]

# Map representative names to indices for checking answer choices
rep_name_to_idx = {
    'Kim': KIM, 'Mahr': MAHR, 'Parra': PARRA,
    'Quinn': QUINN, 'Stuckey': STUCKEY, 'Tiao': TIAO, 'Udall': UDALL
}

# Create reverse mapping: index -> name
rep_idx_to_name = {v: k for k, v in rep_name_to_idx.items()}

# Check each answer choice
answer_index_list = []
for idx, reps in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint: exactly these representatives are in Zone 3
    for i in range(7):
        if rep_idx_to_name[i] in reps:
            # This representative is in the list, so must be in Zone 3
            s_chk.add(zone[i] == 3)
        else:
            # This representative is not in the list, so must NOT be in Zone 3
            s_chk.add(zone[i] != 3)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Output the index of the only SAT choice (as per LSAT format, exactly one should be SAT)
print(answer_index_list[0] if answer_index_list else -1)