from z3 import *

# Representative indices
(K, M, P, Q, S, T, U) = range(7)

# Zone assignment variables: 1, 2, or 3
zones = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each zone is 1, 2, or 3
for z in zones:
    solver.add(Or(z == 1, z == 2, z == 3))

# Zone 1 constraint: exactly one of Parra (P) or Tiao (T) is in Zone 1
solver.add(Or(
    And(zones[P] == 1, zones[T] != 1),
    And(zones[T] == 1, zones[P] != 1)
))

# Zone 2 constraint: exactly one of Tiao (T) or Udall (U) is in Zone 2
solver.add(Or(
    And(zones[T] == 2, zones[U] != 2),
    And(zones[U] == 2, zones[T] != 2)
))

# Parra and Quinn must be in the same zone
solver.add(zones[P] == zones[Q])

# Stuckey and Udall must be in the same zone
solver.add(zones[S] == zones[U])

# Zone 3 has more representatives than Zone 2
zone_counts = [
    Sum([If(zones[i] == 1, 1, 0) for i in range(7)]),
    Sum([If(zones[i] == 2, 1, 0) for i in range(7)]),
    Sum([If(zones[i] == 3, 1, 0) for i in range(7)])
]
solver.add(zone_counts[2] > zone_counts[1])

# Answer choices: list of representatives in Zone 3
answer_choices = [
    ['Kim', 'Mahr'],                    # indices: K, M
    ['Kim', 'Tiao'],                   # indices: K, T
    ['Parra', 'Quinn'],                # indices: P, Q
    ['Stuckey', 'Tiao', 'Udall'],      # indices: S, T, U
    ['Parra', 'Quinn', 'Stuckey', 'Udall']  # indices: P, Q, S, U
]

# Map names to indices for easier reference
name_to_idx = {
    'Kim': K, 'Mahr': M, 'Parra': P,
    'Quinn': Q, 'Stuckey': S, 'Tiao': T, 'Udall': U
}

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Get indices of reps in this choice
    choice_indices = [name_to_idx[name] for name in choice]
    
    # Assert that reps in the choice are in Zone 3
    for rep_idx in choice_indices:
        s_chk.add(zones[rep_idx] == 3)
    
    # Assert that reps NOT in the choice are NOT in Zone 3
    for rep_idx in range(7):
        if rep_idx not in choice_indices:
            s_chk.add(Or(zones[rep_idx] == 1, zones[rep_idx] == 2))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)