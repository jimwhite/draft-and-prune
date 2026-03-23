from z3 import *

# Representative indices: Kim=0, Mahr=1, Parra=2, Quinn=3, Stuckey=4, Tiao=5, Udall=6
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each zone is 1, 2, or 3
for i in range(7):
    solver.add(zone[i] >= 1, zone[i] <= 3)

# Parra or Tiao (but not both) in Zone 1: XOR
solver.add((zone[2] == 1) != (zone[5] == 1))

# Tiao or Udall (but not both) in Zone 2: XOR
solver.add((zone[5] == 2) != (zone[6] == 2))

# Parra and Quinn in same zone
solver.add(zone[2] == zone[3])

# Stuckey and Udall in same zone
solver.add(zone[4] == zone[6])

# More reps in Zone 3 than Zone 2
c1 = Sum([If(zone[i] == 1, 1, 0) for i in range(7)])
c2 = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
c3 = Sum([If(zone[i] == 3, 1, 0) for i in range(7)])
solver.add(c3 > c2)

# Answer choices
answer_choices = [
    # Zone 1: Kim, Parra; Zone 2: Stuckey, Udall; Zone 3: Mahr, Quinn, Tiao
    {"Kim": 1, "Parra": 1, "Stuckey": 2, "Udall": 2, "Mahr": 3, "Quinn": 3, "Tiao": 3},
    # Zone 1: Kim, Tiao; Zone 2: Stuckey, Udall; Zone 3: Mahr, Parra, Quinn
    {"Kim": 1, "Tiao": 1, "Stuckey": 2, "Udall": 2, "Mahr": 3, "Parra": 3, "Quinn": 3},
    # Zone 1: Parra, Quinn; Zone 2: Kim, Udall; Zone 3: Mahr, Stuckey, Tiao
    {"Parra": 1, "Quinn": 1, "Kim": 2, "Udall": 2, "Mahr": 3, "Stuckey": 3, "Tiao": 3},
    # Zone 1: Stuckey, Udall; Zone 2: Kim, Tiao; Zone 3: Mahr, Parra, Quinn
    {"Stuckey": 1, "Udall": 1, "Kim": 2, "Tiao": 2, "Mahr": 3, "Parra": 3, "Quinn": 3},
    # Zone 1: Tiao; Zone 2: Kim, Parra, Quinn; Zone 3: Stuckey, Udall
    {"Tiao": 1, "Kim": 2, "Parra": 2, "Quinn": 2, "Stuckey": 3, "Udall": 3}
]

# Map names to indices
name_to_idx = {
    "Kim": 0, "Mahr": 1, "Parra": 2, "Quinn": 3,
    "Stuckey": 4, "Tiao": 5, "Udall": 6
}

# Check each answer choice
answer_index_list = []
for idx, assignment in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add specific assignments for this choice
    for name, zone_id in assignment.items():
        s_chk.add(zone[name_to_idx[name]] == zone_id)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)