from z3 import *

# Representative indices: Kim=0, Mahr=1, Parra=2, Quinn=3, Stuckey=4, Tiao=5, Udall=6
rep_names = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]
rep_indices = {name: i for i, name in enumerate(rep_names)}

# Zone variables
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Each representative is assigned exactly one zone (1, 2, or 3)
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Parra or Tiao (but not both) in Zone 1
solver.add(Xor(zone[rep_indices["Parra"]] == 1, zone[rep_indices["Tiao"]] == 1))

# Tiao or Udall (but not both) in Zone 2
solver.add(Xor(zone[rep_indices["Tiao"]] == 2, zone[rep_indices["Udall"]] == 2))

# Parra and Quinn in same zone
solver.add(zone[rep_indices["Parra"]] == zone[rep_indices["Quinn"]])

# Stuckey and Udall in same zone
solver.add(zone[rep_indices["Stuckey"]] == zone[rep_indices["Udall"]])

# Zone count constraint: more reps in Zone 3 than in Zone 2
count3 = Sum([If(zone[i] == 3, 1, 0) for i in range(7)])
count2 = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
solver.add(count3 > count2)

# Answer choices
answer_choices = [
    ["Kim", "Mahr"],                    # indices {0, 1}
    ["Kim", "Tiao"],                   # indices {0, 5}
    ["Parra", "Quinn"],                # indices {2, 3}
    ["Stuckey", "Tiao", "Udall"],     # indices {4, 5, 6}
    ["Parra", "Quinn", "Stuckey", "Udall"]  # indices {2, 3, 4, 6}
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Convert choice to set of indices
    choice_set = {rep_indices[name] for name in choice}
    
    # Enforce that exactly these representatives are in Zone 3
    for i in range(7):
        if i in choice_set:
            s_chk.add(zone[i] == 3)
        else:
            s_chk.add(zone[i] != 3)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)