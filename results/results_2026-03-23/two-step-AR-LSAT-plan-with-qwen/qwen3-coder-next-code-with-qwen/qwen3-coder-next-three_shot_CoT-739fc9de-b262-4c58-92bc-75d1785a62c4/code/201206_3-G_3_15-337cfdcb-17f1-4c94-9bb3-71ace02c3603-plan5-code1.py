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

# Zone 1 constraint: exactly one of Parra or Tiao is in Zone 1
solver.add(Xor(zone[PARRA] == 1, zone[TIAO] == 1))

# Zone 2 constraint: exactly one of Tiao or Udall is in Zone 2
solver.add(Xor(zone[TIAO] == 2, zone[UDALL] == 2))

# Parra and Quinn in same zone
solver.add(zone[PARRA] == zone[QUINN])

# Stuckey and Udall in same zone
solver.add(zone[STUCKEY] == zone[UDALL])

# Zone 3 has more representatives than Zone 2
count_zone3 = Sum([If(zone[i] == 3, 1, 0) for i in range(7)])
count_zone2 = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
solver.add(count_zone3 > count_zone2)

# Answer choices
answer_choices = [
    ["Kim", "Mahr"],                    # index 0: Kim, Mahr in Zone 3
    ["Kim", "Tiao"],                   # index 1: Kim, Tiao in Zone 3
    ["Parra", "Quinn"],                # index 2: Parra, Quinn in Zone 3
    ["Stuckey", "Tiao", "Udall"],     # index 3: Stuckey, Tiao, Udall in Zone 3
    ["Parra", "Quinn", "Stuckey", "Udall"]  # index 4: Parra, Quinn, Stuckey, Udall in Zone 3
]

# Map representative names to indices for answer checking
rep_name_to_idx = {
    "Kim": KIM,
    "Mahr": MAHR,
    "Parra": PARRA,
    "Quinn": QUINN,
    "Stuckey": STUCKEY,
    "Tiao": TIAO,
    "Udall": UDALL
}

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints: representatives in the choice must be in Zone 3
    for rep_name in choice:
        s_chk.add(zone[rep_name_to_idx[rep_name]] == 3)
    
    # Check if this assignment is possible
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)