from z3 import *

# Representative indices: Kim=0, Mahr=1, Parra=2, Quinn=3, Stuckey=4, Tiao=5, Udall=6
names = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]
indices = {name: i for i, name in enumerate(names)}

# Zone variables
z = [Int(f"z_{name}") for name in names]

# Base solver
solver = Solver()

# Each representative assigned exactly one zone (1, 2, or 3)
for i in range(7):
    solver.add(Or(z[i] == 1, z[i] == 2, z[i] == 3))

# Zone 1: Exactly one of Parra or Tiao
solver.add(Xor(z[indices["Parra"]] == 1, z[indices["Tiao"]] == 1))

# Zone 2: Exactly one of Tiao or Udall
solver.add(Xor(z[indices["Tiao"]] == 2, z[indices["Udall"]] == 2))

# Parra and Quinn in same zone
solver.add(z[indices["Parra"]] == z[indices["Quinn"]])

# Stuckey and Udall in same zone
solver.add(z[indices["Stuckey"]] == z[indices["Udall"]])

# Zone size constraint: more in Zone 3 than Zone 2
count_zone = lambda zone: Sum([If(z[i] == zone, 1, 0) for i in range(7)])
solver.add(count_zone(3) > count_zone(2))

# Answer choices
answer_choices = [
    ["Kim", "Mahr"],                    # Choice 0: Zone 3 = {Kim, Mahr}
    ["Kim", "Tiao"],                   # Choice 1: Zone 3 = {Kim, Tiao}
    ["Parra", "Quinn"],                # Choice 2: Zone 3 = {Parra, Quinn}
    ["Stuckey", "Tiao", "Udall"],     # Choice 3: Zone 3 = {Stuckey, Tiao, Udall}
    ["Parra", "Quinn", "Stuckey", "Udall"]  # Choice 4: Zone 3 = {Parra, Quinn, Stuckey, Udall}
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # All reps in choice must be in Zone 3
    for name in choice:
        s_chk.add(z[indices[name]] == 3)
    
    # All reps not in choice must NOT be in Zone 3
    for name in names:
        if name not in choice:
            s_chk.add(z[indices[name]] != 3)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)