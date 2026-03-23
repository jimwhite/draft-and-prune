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

# Parra or Tiao (but not both) in Zone 1
solver.add(Or(
    And(zone[PARRA] == 1, zone[TIAO] != 1),
    And(zone[TIAO] == 1, zone[PARRA] != 1)
))

# Tiao or Udall (but not both) in Zone 2
solver.add(Or(
    And(zone[TIAO] == 2, zone[UDALL] != 2),
    And(zone[UDALL] == 2, zone[TIAO] != 2)
))

# Parra and Quinn in same zone
solver.add(zone[PARRA] == zone[QUINN])

# Stuckey and Udall in same zone
solver.add(zone[STUCKEY] == zone[UDALL])

# Zone 3 has more representatives than Zone 2
count_zone = lambda z: Sum([If(zone[i] == z, 1, 0) for i in range(7)])
solver.add(count_zone(3) > count_zone(2))

# Answer choices
answer_choices = [
    ["KIM", "MAHR"],           # 0: Kim, Mahr
    ["KIM", "TIAO"],          # 1: Kim, Tiao
    ["PARRA", "QUINN"],       # 2: Parra, Quinn
    ["STUCKEY", "TIAO", "UDALL"],  # 3: Stuckey, Tiao, Udall
    ["PARRA", "QUINN", "STUCKEY", "UDALL"]  # 4: Parra, Quinn, Stuckey, Udall
]

# Map names to indices for checking
name_to_idx = {
    "KIM": KIM, "MAHR": MAHR, "PARRA": PARRA,
    "QUINN": QUINN, "STUCKEY": STUCKEY, "TIAO": TIAO, "UDALL": UDALL
}

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Get set of representatives in Zone 3 for this choice
    zone3_reps = [name_to_idx[name] for name in choice]
    
    # Assert that exactly these representatives are in Zone 3
    for i in range(7):
        if i in zone3_reps:
            s_chk.add(zone[i] == 3)
        else:
            s_chk.add(zone[i] != 3)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)