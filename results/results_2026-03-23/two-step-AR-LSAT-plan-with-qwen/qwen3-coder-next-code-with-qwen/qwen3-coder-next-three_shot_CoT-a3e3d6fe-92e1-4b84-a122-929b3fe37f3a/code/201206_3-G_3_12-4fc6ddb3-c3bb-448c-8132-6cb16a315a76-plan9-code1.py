from z3 import *

# Representative indices
(K, M, P, Q, S, T, U) = range(7)

# Zone variables: 1, 2, or 3
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each zone is 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Zone 1 constraint: exactly one of Parra (2) or Tiao (5)
solver.add(Or(
    And(zone[P] == 1, zone[T] != 1),
    And(zone[T] == 1, zone[P] != 1)
))

# Zone 2 constraint: exactly one of Tiao (5) or Udall (6)
solver.add(Or(
    And(zone[T] == 2, zone[U] != 2),
    And(zone[U] == 2, zone[T] != 2)
))

# Parra and Quinn in same zone
solver.add(zone[P] == zone[Q])

# Stuckey and Udall in same zone
solver.add(zone[S] == zone[U])

# Zone size constraint: Zone 3 > Zone 2
zone_count = lambda z: Sum([If(zone[i] == z, 1, 0) for i in range(7)])
solver.add(zone_count(3) > zone_count(2))

# Answer choices
choices = [
    # Zone 1: Kim, Parra; Zone 2: Stuckey, Udall; Zone 3: Mahr, Quinn, Tiao
    {K:1, P:1, S:2, U:2, M:3, Q:3, T:3},
    # Zone 1: Kim, Tiao; Zone 2: Stuckey, Udall; Zone 3: Mahr, Parra, Quinn
    {K:1, T:1, S:2, U:2, M:3, P:3, Q:3},
    # Zone 1: Parra, Quinn; Zone 2: Kim, Udall; Zone 3: Mahr, Stuckey, Tiao
    {P:1, Q:1, K:2, U:2, M:3, S:3, T:3},
    # Zone 1: Stuckey, Udall; Zone 2: Kim, Tiao; Zone 3: Mahr, Parra, Quinn
    {S:1, U:1, K:2, T:2, M:3, P:3, Q:3},
    # Zone 1: Tiao; Zone 2: Kim, Parra, Quinn; Zone 3: Stuckey, Udall
    {T:1, K:2, P:2, Q:2, S:3, U:3}
]

answer_index_list = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the proposed assignments
    for rep, z in choice.items():
        s_chk.add(zone[rep] == z)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Output the first valid choice's full text
if answer_index_list:
    print(f"Choice {answer_index_list[0]}: {choices[answer_index_list[0]]}")
else:
    print("No valid choice found")