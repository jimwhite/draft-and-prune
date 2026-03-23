from z3 import *

# Representative indices
(KIM, MAHR, PARRA, QUINN, STUCKEY, TIAO, UDALL) = range(7)

# Zone variables: zone[i] is the zone (1, 2, or 3) for representative i
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each zone is 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Zone 1 constraint: exactly one of Parra or Tiao is in Zone 1
solver.add(Xor(zone[PARRA] == 1, zone[TIAO] == 1))

# Zone 2 constraint: exactly one of Tiao or Udall is in Zone 2
solver.add(Xor(zone[TIAO] == 2, zone[UDALL] == 2))

# Parra and Quinn in same zone
solver.add(zone[PARRA] == zone[QUINN])

# Stuckey and Udall in same zone
solver.add(zone[STUCKEY] == zone[UDALL])

# Zone size constraint: more representatives in Zone 3 than in Zone 2
c1 = Sum([If(zone[i] == 1, 1, 0) for i in range(7)])
c2 = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
c3 = Sum([If(zone[i] == 3, 1, 0) for i in range(7)])
solver.add(c3 > c2)

# Answer choices
answer_choices = [
    ["Kim", "Mahr"],  # indices: KIM, MAHR
    ["Kim", "Tiao"],  # indices: KIM, TIAO
    ["Parra", "Quinn"],  # indices: PARRA, QUINN
    ["Stuckey", "Tiao", "Udall"],  # indices: STUCKEY, TIAO, UDALL
    ["Parra", "Quinn", "Stuckey", "Udall"]  # indices: PARRA, QUINN, STUCKEY, UDALL
]

# Map names to indices for checking
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
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Get indices of representatives in this choice
    choice_indices = set(name_to_idx[name] for name in choice)
    
    # Assert zone 3 exactly for representatives in the choice
    for i in range(7):
        if i in choice_indices:
            s_chk.add(zone[i] == 3)
        else:
            s_chk.add(zone[i] != 3)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Print the index of the correct answer (only one should be SAT)
print(answer_index_list)