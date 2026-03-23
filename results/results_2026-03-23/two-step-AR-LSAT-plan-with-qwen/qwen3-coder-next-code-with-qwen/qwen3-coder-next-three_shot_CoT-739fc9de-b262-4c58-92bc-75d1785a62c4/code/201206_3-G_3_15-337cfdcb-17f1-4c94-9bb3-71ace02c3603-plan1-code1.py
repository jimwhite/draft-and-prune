from z3 import *

# Representative indices
(KIM, MAHR, PARRA, QUINN, STUCKEY, TIAO, UDALL) = range(7)

# Zone variables: zone[i] is the zone (1, 2, or 3) for representative i
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each representative assigned to exactly one zone (1, 2, or 3)
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Parra or Tiao (but not both) in Zone 1
solver.add(Xor(zone[PARRA] == 1, zone[TIAO] == 1))

# Tiao or Udall (but not both) in Zone 2
solver.add(Xor(zone[TIAO] == 2, zone[UDALL] == 2))

# Parra and Quinn in same zone
solver.add(zone[PARRA] == zone[QUINN])

# Stuckey and Udall in same zone
solver.add(zone[STUCKEY] == zone[UDALL])

# Zone 3 has more representatives than Zone 2
c1 = Sum([If(zone[i] == 1, 1, 0) for i in range(7)])
c2 = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
c3 = Sum([If(zone[i] == 3, 1, 0) for i in range(7)])
solver.add(c3 > c2)

# Answer choices
answer_choices = [
    ['Kim', 'Mahr'],           # 0: Kim and Mahr in Zone 3
    ['Kim', 'Tiao'],           # 1: Kim and Tiao in Zone 3
    ['Parra', 'Quinn'],        # 2: Parra and Quinn in Zone 3
    ['Stuckey', 'Tiao', 'Udall'], # 3: Stuckey, Tiao, Udall in Zone 3
    ['Parra', 'Quinn', 'Stuckey', 'Udall'] # 4: Parra, Quinn, Stuckey, Udall in Zone 3
]

# Map names to indices for easier reference
rep_name_to_idx = {
    'Kim': KIM, 'Mahr': MAHR, 'Parra': PARRA,
    'Quinn': QUINN, 'Stuckey': STUCKEY, 'Tiao': TIAO, 'Udall': UDALL
}

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Get set of reps in Zone 3 from this choice
    zone3_reps = [rep_name_to_idx[name] for name in choice]
    
    # Assert exactly these reps are in Zone 3
    for i in range(7):
        if i in zone3_reps:
            s_chk.add(zone[i] == 3)
        else:
            s_chk.add(zone[i] != 3)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)