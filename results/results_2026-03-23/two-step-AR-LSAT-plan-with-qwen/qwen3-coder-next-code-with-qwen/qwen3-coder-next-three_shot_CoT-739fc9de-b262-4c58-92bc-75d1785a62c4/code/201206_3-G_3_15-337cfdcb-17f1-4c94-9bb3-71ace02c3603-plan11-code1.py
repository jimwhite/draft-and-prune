from z3 import *

# Representative indices
(KIM, MAHR, PARRA, QUINN, STU, TIAO, UDALL) = range(7)

# Zone variables: zone[i] = zone number (1, 2, or 3) for representative i
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each representative is assigned to zone 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Zone 1 constraint: exactly one of Parra or Tiao is in Zone 1 (XOR)
solver.add(Or(
    And(zone[PARRA] == 1, zone[TIAO] != 1),
    And(zone[TIAO] == 1, zone[PARRA] != 1)
))

# Zone 2 constraint: exactly one of Tiao or Udall is in Zone 2 (XOR)
solver.add(Or(
    And(zone[TIAO] == 2, zone[UDALL] != 2),
    And(zone[UDALL] == 2, zone[TIAO] != 2)
))

# Parra and Quinn work in the same zone
solver.add(zone[PARRA] == zone[QUINN])

# Stuckey and Udall work in the same zone
solver.add(zone[STU] == zone[UDALL])

# Zone size constraint: more representatives in Zone 3 than in Zone 2
count_zone = lambda z: Sum([If(zone[i] == z, 1, 0) for i in range(7)])
solver.add(count_zone(3) > count_zone(2))

# Answer choices
answer_choices = [
    ["Kim", "Mahr"],                    # 0: Kim, Mahr in Zone 3
    ["Kim", "Tiao"],                    # 1: Kim, Tiao in Zone 3
    ["Parra", "Quinn"],                 # 2: Parra, Quinn in Zone 3
    ["Stuckey", "Tiao", "Udall"],      # 3: Stuckey, Tiao, Udall in Zone 3
    ["Parra", "Quinn", "Stuckey", "Udall"]  # 4: Parra, Quinn, Stuckey, Udall in Zone 3
]

# Map names to indices for easier reference
name_to_idx = {
    "Kim": KIM, "Mahr": MAHR, "Parra": PARRA,
    "Quinn": QUINN, "Stuckey": STU, "Tiao": TIAO, "Udall": UDALL
}

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assign representatives in the choice to Zone 3
    for name in choice:
        s_chk.add(zone[name_to_idx[name]] == 3)
    
    # Derive additional constraints based on the answer choice and base rules
    # Parra-Quinn must be together (already handled by base constraint)
    # Stuckey-Udall must be together (already handled by base constraint)
    
    # Check consistency with Zone 1 and Zone 2 XOR constraints
    # If Parra is in Zone 3, then from Zone 1 XOR: Tiao must be in Zone 1
    if "Parra" in choice:
        # Parra is in Zone 3, so Tiao must be in Zone 1 (from Zone 1 XOR)
        s_chk.add(zone[TIAO] == 1)
    else:
        # Parra is not in Zone 3, so Tiao must be in Zone 1 (from Zone 1 XOR)
        s_chk.add(zone[PARRA] != 3)  # Parra not in Zone 3
        s_chk.add(zone[TIAO] == 1)
    
    # If Tiao is in Zone 3, then from Zone 2 XOR: Udall must be in Zone 1 or 3 (but not Zone 2)
    # But Stuckey-Udall must be together, so if Udall is not in Zone 2, they could be in Zone 1 or 3
    if "Tiao" in choice:
        # Tiao is in Zone 3, so from Zone 2 XOR: Udall must NOT be in Zone 2
        s_chk.add(zone[UDALL] != 2)
    else:
        # Tiao is not in Zone 3, so from Zone 2 XOR: Udall must be in Zone 2
        s_chk.add(zone[UDALL] == 2)
    
    # Check if the model is satisfiable
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)