from z3 import *

# Representative indices
(K, M, P, Q, S, T, U) = range(7)

# Zone variables: zone[i] = zone assignment for representative i (1, 2, or 3)
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each representative assigned to zone 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Parra or Tiao (but not both) in Zone 1
solver.add(Or(
    And(zone[P] == 1, zone[T] != 1),
    And(zone[T] == 1, zone[P] != 1)
))

# Tiao or Udall (but not both) in Zone 2
solver.add(Or(
    And(zone[T] == 2, zone[U] != 2),
    And(zone[U] == 2, zone[T] != 2)
))

# Parra and Quinn in same zone
solver.add(zone[P] == zone[Q])

# Stuckey and Udall in same zone
solver.add(zone[S] == zone[U])

# Zone 3 has more representatives than Zone 2
count_zone = lambda z: Sum([If(zone[i] == z, 1, 0) for i in range(7)])
solver.add(count_zone(3) > count_zone(2))

# Answer choices
answer_choices = [
    # Zone 1: Kim, Parra; Zone 2: Stuckey, Udall; Zone 3: Mahr, Quinn, Tiao
    {K: 1, P: 1, S: 2, U: 2, M: 3, Q: 3, T: 3},
    # Zone 1: Kim, Tiao; Zone 2: Stuckey, Udall; Zone 3: Mahr, Parra, Quinn
    {K: 1, T: 1, S: 2, U: 2, M: 3, P: 3, Q: 3},
    # Zone 1: Parra, Quinn; Zone 2: Kim, Udall; Zone 3: Mahr, Stuckey, Tiao
    {P: 1, Q: 1, K: 2, U: 2, M: 3, S: 3, T: 3},
    # Zone 1: Stuckey, Udall; Zone 2: Kim, Tiao; Zone 3: Mahr, Parra, Quinn
    {S: 1, U: 1, K: 2, T: 2, M: 3, P: 3, Q: 3},
    # Zone 1: Tiao; Zone 2: Kim, Parra, Quinn; Zone 3: Stuckey, Udall
    {T: 1, K: 2, P: 2, Q: 2, S: 3, U: 3}
]

# Check each answer choice
answer_index_list = []
for idx, assignment in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the zone assignments from this choice
    for rep, z in assignment.items():
        s_chk.add(zone[rep] == z)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)