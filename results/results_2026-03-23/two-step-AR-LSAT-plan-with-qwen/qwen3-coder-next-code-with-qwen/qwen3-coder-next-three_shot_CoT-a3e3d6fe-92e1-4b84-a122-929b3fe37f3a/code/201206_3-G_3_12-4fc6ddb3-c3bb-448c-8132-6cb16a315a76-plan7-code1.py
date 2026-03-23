from z3 import *

# Representative indices: Kim=0, Mahr=1, Parra=2, Quinn=3, Stuckey=4, Tiao=5, Udall=6
reps = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]
zone_vars = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each rep assigned to zone 1, 2, or 3
for i in range(7):
    solver.add(zone_vars[i] >= 1, zone_vars[i] <= 3)

# Zone 1 constraint: Exactly one of Parra (2) or Tiao (5) is in Zone 1
solver.add(Or(
    And(zone_vars[2] == 1, zone_vars[5] != 1),
    And(zone_vars[2] != 1, zone_vars[5] == 1)
))

# Zone 2 constraint: Exactly one of Tiao (5) or Udall (6) is in Zone 2
solver.add(Or(
    And(zone_vars[5] == 2, zone_vars[6] != 2),
    And(zone_vars[5] != 2, zone_vars[6] == 2)
))

# Parra and Quinn same zone constraint
solver.add(zone_vars[2] == zone_vars[3])

# Stuckey and Udall same zone constraint
solver.add(zone_vars[4] == zone_vars[6])

# Zone size constraint: Zone 3 > Zone 2
zone_count = lambda z: Sum([If(zone_vars[i] == z, 1, 0) for i in range(7)])
solver.add(zone_count(3) > zone_count(2))

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

# Check each answer choice
valid_indices = []
for idx, assignment in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific assignment constraints
    rep_to_idx = {"Kim": 0, "Mahr": 1, "Parra": 2, "Quinn": 3, "Stuckey": 4, "Tiao": 5, "Udall": 6}
    for rep, zone in assignment.items():
        s_chk.add(zone_vars[rep_to_idx[rep]] == zone)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)