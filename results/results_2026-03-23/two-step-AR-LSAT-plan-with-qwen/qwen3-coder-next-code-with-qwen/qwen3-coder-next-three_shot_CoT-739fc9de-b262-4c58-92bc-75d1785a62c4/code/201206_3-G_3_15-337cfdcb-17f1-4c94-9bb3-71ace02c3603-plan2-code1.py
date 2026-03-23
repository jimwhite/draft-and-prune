from z3 import *

# Representative indices: Kim=0, Mahr=1, Parra=2, Quinn=3, Stuckey=4, Tiao=5, Udall=6
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each zone is 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Zone 1 constraint: exactly one of Parra (2) or Tiao (5)
solver.add(Xor(zone[2] == 1, zone[5] == 1))

# Zone 2 constraint: exactly one of Tiao (5) or Udall (6)
solver.add(Xor(zone[5] == 2, zone[6] == 2))

# Parra and Quinn same zone
solver.add(zone[2] == zone[3])

# Stuckey and Udall same zone
solver.add(zone[4] == zone[6])

# Zone size constraint: count in Zone 3 > count in Zone 2
count1 = Sum([If(zone[i] == 1, 1, 0) for i in range(7)])
count2 = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
count3 = Sum([If(zone[i] == 3, 1, 0) for i in range(7)])
solver.add(count3 > count2)

# Answer choices
answer_choices = [
    ["Kim", "Mahr"],                    # indices [0, 1]
    ["Kim", "Tiao"],                   # indices [0, 5]
    ["Parra", "Quinn"],                # indices [2, 3]
    ["Stuckey", "Tiao", "Udall"],     # indices [4, 5, 6]
    ["Parra", "Quinn", "Stuckey", "Udall"]  # indices [2, 3, 4, 6]
]

# Map names to indices
name_to_idx = {
    "Kim": 0, "Mahr": 1, "Parra": 2, "Quinn": 3,
    "Stuckey": 4, "Tiao": 5, "Udall": 6
}

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Get indices of representatives in this choice
    choice_indices = [name_to_idx[name] for name in choice]
    
    # Add constraints: representatives in choice must be in Zone 3, others not in Zone 3
    for i in range(7):
        if i in choice_indices:
            s_chk.add(zone[i] == 3)
        else:
            s_chk.add(zone[i] != 3)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)