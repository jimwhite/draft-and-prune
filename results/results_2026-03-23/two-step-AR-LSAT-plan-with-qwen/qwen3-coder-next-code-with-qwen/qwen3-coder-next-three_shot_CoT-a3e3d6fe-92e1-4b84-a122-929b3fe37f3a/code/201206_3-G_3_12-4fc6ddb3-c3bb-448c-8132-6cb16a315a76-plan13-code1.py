from z3 import *

# Representative indices
(KIM, MAHR, PARRA, QUINN, STUCKEY, TIAO, UDALL) = range(7)

# Zone variables for each representative
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each zone is 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Parra/Tiao Zone 1 constraint: exactly one of them is in Zone 1
solver.add(Xor(zone[PARRA] == 1, zone[TIAO] == 1))

# Tiao/Udall Zone 2 constraint: exactly one of them is in Zone 2
solver.add(Xor(zone[TIAO] == 2, zone[UDALL] == 2))

# Parra and Quinn work in the same zone
solver.add(zone[PARRA] == zone[QUINN])

# Stuckey and Udall work in the same zone
solver.add(zone[STUCKEY] == zone[UDALL])

# Zone 3 size > Zone 2 size
count_zone1 = Sum([If(zone[i] == 1, 1, 0) for i in range(7)])
count_zone2 = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
count_zone3 = Sum([If(zone[i] == 3, 1, 0) for i in range(7)])
solver.add(count_zone3 > count_zone2)

# Answer choices
answer_choices = [
    # Zone 1: Kim, Parra; Zone 2: Stuckey, Udall; Zone 3: Mahr, Quinn, Tiao
    {KIM: 1, MAHR: 3, PARRA: 1, QUINN: 3, STUCKEY: 2, TIAO: 3, UDALL: 2},
    # Zone 1: Kim, Tiao; Zone 2: Stuckey, Udall; Zone 3: Mahr, Parra, Quinn
    {KIM: 1, MAHR: 3, PARRA: 3, QUINN: 3, STUCKEY: 2, TIAO: 1, UDALL: 2},
    # Zone 1: Parra, Quinn; Zone 2: Kim, Udall; Zone 3: Mahr, Stuckey, Tiao
    {KIM: 2, MAHR: 3, PARRA: 1, QUINN: 1, STUCKEY: 3, TIAO: 3, UDALL: 2},
    # Zone 1: Stuckey, Udall; Zone 2: Kim, Tiao; Zone 3: Mahr, Parra, Quinn
    {KIM: 2, MAHR: 3, PARRA: 3, QUINN: 3, STUCKEY: 1, TIAO: 2, UDALL: 1},
    # Zone 1: Tiao; Zone 2: Kim, Parra, Quinn; Zone 3: Stuckey, Udall
    {KIM: 2, MAHR: 3, PARRA: 2, QUINN: 2, STUCKEY: 3, TIAO: 1, UDALL: 3}
]

# Check each answer choice
answer_index_list = []
for idx, assignment in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the proposed assignment constraints
    for rep, zone_num in assignment.items():
        s_chk.add(zone[rep] == zone_num)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)