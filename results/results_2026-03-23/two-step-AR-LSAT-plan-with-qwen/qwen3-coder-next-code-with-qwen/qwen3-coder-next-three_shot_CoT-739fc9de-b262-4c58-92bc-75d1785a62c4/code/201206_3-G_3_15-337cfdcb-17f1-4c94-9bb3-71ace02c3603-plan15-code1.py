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

# Exclusive-or constraints
# Zone 1: exactly one of Parra or Tiao (i.e., one is in zone 1, the other is not)
solver.add(Or(
    And(zone[PARRA] == 1, zone[TIAO] != 1),
    And(zone[TIAO] == 1, zone[PARRA] != 1)
))

# Zone 2: exactly one of Tiao or Udall (i.e., one is in zone 2, the other is not)
solver.add(Or(
    And(zone[TIAO] == 2, zone[UDALL] != 2),
    And(zone[UDALL] == 2, zone[TIAO] != 2)
))

# Equivalence constraints
# Parra and Quinn in same zone
solver.add(zone[PARRA] == zone[QUINN])
# Stuckey and Udall in same zone
solver.add(zone[STUCKEY] == zone[UDALL])

# Zone size constraint: more representatives in Zone 3 than in Zone 2
zone_count = lambda z: Sum([If(zone[i] == z, 1, 0) for i in range(7)])
solver.add(zone_count(3) > zone_count(2))

# Answer choices: list of sets of representatives in Zone 3
answer_choices = [
    {"Kim", "Mahr"},
    {"Kim", "Tiao"},
    {"Parra", "Quinn"},
    {"Stuckey", "Tiao", "Udall"},
    {"Parra", "Quinn", "Stuckey", "Udall"}
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
answer_index_list = []
for idx, choice_set in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Enforce that exactly the representatives in choice_set are in Zone 3
    for name, idx_rep in name_to_idx.items():
        if name in choice_set:
            s_chk.add(zone[idx_rep] == 3)
        else:
            s_chk.add(zone[idx_rep] != 3)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)