from z3 import *

# Representative indices
(KIM, MAHR, PARRA, QUINN, STUCKEY, TIAO, UDALL) = range(7)

# Zone variables: zone[i] = zone number (1, 2, or 3) for representative i
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Zone domain constraints: each representative assigned to zone 1, 2, or 3
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
solver.add(zone[STUCKEY] == zone[UDALL])

# Zone size constraint: more representatives in Zone 3 than in Zone 2
count_zone = lambda z: Sum([If(zone[i] == z, 1, 0) for i in range(7)])
solver.add(count_zone(3) > count_zone(2))

# Answer choices
answer_choices = [
    ["Kim", "Mahr"],
    ["Kim", "Tiao"],
    ["Parra", "Quinn"],
    ["Stuckey", "Tiao", "Udall"],
    ["Parra", "Quinn", "Stuckey", "Udall"]
]

# Map names to indices
name_to_idx = {
    "Kim": KIM,
    "Mahr": MAHR,
    "Parra": PARRA,
    "Quinn": QUINN,
    "Stuckey": STUCKEY,
    "Tiao": TIAO,
    "Udall": UDALL
}

# Check each answer choice
valid_choices = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert exact membership of Zone 3
    for name in ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]:
        rep_idx = name_to_idx[name]
        if name in choice:
            s_chk.add(zone[rep_idx] == 3)
        else:
            s_chk.add(Or(zone[rep_idx] != 3))
    
    if s_chk.check() == sat:
        valid_choices.append(idx)

# Print the index of the valid choice (only one should be valid)
print(valid_choices[0] if len(valid_choices) == 1 else valid_choices)