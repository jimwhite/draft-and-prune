from z3 import *

# Representative indices
(KIM, MAHR, PARRA, QUINN, STUCKEY, TIAO, UDALL) = range(7)

# Zone assignment variables: zone[i] = zone number (1, 2, or 3) for representative i
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each representative assigned to zone 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Mutual exclusion constraints
# (Parra in Zone 1) XOR (Tiao in Zone 1)
solver.add(Xor(zone[PARRA] == 1, zone[TIAO] == 1))

# (Tiao in Zone 2) XOR (Udall in Zone 2)
solver.add(Xor(zone[TIAO] == 2, zone[UDALL] == 2))

# Parra and Quinn in same zone
solver.add(zone[PARRA] == zone[QUINN])

# Stuckey and Udall in same zone
solver.add(zone[STUCKEY] == zone[UDALL])

# Zone size constraint: more representatives in Zone 3 than in Zone 2
count_zone = lambda z: Sum([If(zone[i] == z, 1, 0) for i in range(7)])
solver.add(count_zone(3) > count_zone(2))

# Answer choices
answer_choices = [
    # Zone 1: Kim, Parra; Zone 2: Stuckey, Udall; Zone 3: Mahr, Quinn, Tiao
    {KIM: 1, PARRA: 1, STUCKEY: 2, UDALL: 2, MAHR: 3, QUINN: 3, TIAO: 3},
    # Zone 1: Kim, Tiao; Zone 2: Stuckey, Udall; Zone 3: Mahr, Parra, Quinn
    {KIM: 1, TIAO: 1, STUCKEY: 2, UDALL: 2, MAHR: 3, PARRA: 3, QUINN: 3},
    # Zone 1: Parra, Quinn; Zone 2: Kim, Udall; Zone 3: Mahr, Stuckey, Tiao
    {PARRA: 1, QUINN: 1, KIM: 2, UDALL: 2, MAHR: 3, STUCKEY: 3, TIAO: 3},
    # Zone 1: Stuckey, Udall; Zone 2: Kim, Tiao; Zone 3: Mahr, Parra, Quinn
    {STUCKEY: 1, UDALL: 1, KIM: 2, TIAO: 2, MAHR: 3, PARRA: 3, QUINN: 3},
    # Zone 1: Tiao; Zone 2: Kim, Parra, Quinn; Zone 3: Stuckey, Udall
    {TIAO: 1, KIM: 2, PARRA: 2, QUINN: 2, STUCKEY: 3, UDALL: 3}
]

# Check each answer choice
answer_index_list = []
for idx, assignments in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add specific assignments from the answer choice
    for rep, z in assignments.items():
        s_chk.add(zone[rep] == z)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)