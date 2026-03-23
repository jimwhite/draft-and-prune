from z3 import *

# Representatives indices: Kim=0, Mahr=1, Parra=2, Quinn=3, Stuckey=4, Tiao=5, Udall=6
names = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]
zone = [Int(f"zone_{i}") for i in range(7)]

solver = Solver()

# Zone domain constraints: each zone is 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Either Parra or Tiao (but not both) works in Zone 1
solver.add(Xor(zone[2] == 1, zone[5] == 1))

# Either Tiao or Udall (but not both) works in Zone 2
solver.add(Xor(zone[5] == 2, zone[6] == 2))

# Parra and Quinn work in the same zone
solver.add(zone[2] == zone[3])

# Stuckey and Udall work in the same zone
solver.add(zone[4] == zone[6])

# More representatives in Zone 3 than in Zone 2
count_zone3 = Sum([If(zone[i] == 3, 1, 0) for i in range(7)])
count_zone2 = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
solver.add(count_zone3 > count_zone2)

# Answer choices
answer_choices = [
    ["Kim", "Mahr"],
    ["Kim", "Tiao"],
    ["Parra", "Quinn"],
    ["Stuckey", "Tiao", "Udall"],
    ["Parra", "Quinn", "Stuckey", "Udall"]
]

# Map names to indices
name_to_idx = {name: i for i, name in enumerate(names)}

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Get set of representatives in Zone 3 for this choice
    zone3_set = {name_to_idx[name] for name in choice}
    
    # Assert Zone 3 members
    for i in range(7):
        if i in zone3_set:
            s_chk.add(zone[i] == 3)
        else:
            s_chk.add(zone[i] != 3)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)