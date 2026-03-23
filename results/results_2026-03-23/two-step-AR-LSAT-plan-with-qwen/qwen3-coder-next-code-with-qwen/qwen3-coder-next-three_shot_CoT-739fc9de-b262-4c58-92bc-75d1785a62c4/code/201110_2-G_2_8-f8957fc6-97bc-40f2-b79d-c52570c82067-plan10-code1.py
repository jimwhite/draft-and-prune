from z3 import *

# Candidate indices: Jaramillo=0, Kayne=1, Landon=2, Novetzke=3, Ong=4
CANDIDATES = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]
J, K, L, N, O = 0, 1, 2, 3, 4

# Country indices: Venezuela=0, Yemen=1, Zambia=2
VENEZUELA, YEMEN, ZAMBIA = 0, 1, 2

# Assignment variables: assigned[country][candidate] is True if candidate is assigned to country
assigned = [[Bool(f"assigned_{c}_{j}") for j in range(5)] for c in range(3)]

# Base solver
solver = Solver()

# One-to-one assignment constraints
## Each country gets exactly one ambassador
for c in range(3):
    solver.add(Sum([If(assigned[c][j], 1, 0) for j in range(5)]) == 1)

## Each candidate assigned to at most one country
for j in range(5):
    solver.add(Sum([If(assigned[c][j], 1, 0) for c in range(3)]) <= 1)

# Candidate constraints
## (a) Exactly one of Kayne or Novetzke is assigned
assigned_to_Kayne = Sum([If(assigned[c][K], 1, 0) for c in range(3)])
assigned_to_Novetzke = Sum([If(assigned[c][N], 1, 0) for c in range(3)])
solver.add(assigned_to_Kayne + assigned_to_Novetzke == 1)

## (b) If Jaramillo is assigned, then Kayne must be assigned
assigned_to_Jaramillo = Sum([If(assigned[c][J], 1, 0) for c in range(3)])
solver.add(Implies(assigned_to_Jaramillo >= 1, assigned_to_Kayne >= 1))

## (c) If Ong is assigned to Venezuela, then Kayne must not be assigned to Yemen
solver.add(Implies(assigned[VENEZUELA][O], Not(assigned[YEMEN][K])))

## (d) If Landon is assigned, it must be to Zambia
solver.add(Not(assigned[VENEZUELA][L]))
solver.add(Not(assigned[YEMEN][L]))

# Answer choices: pairs of candidates who are NOT assigned
answer_choices = [
    (J, N),  # Jaramillo and Novetzke
    (J, O),  # Jaramillo and Ong
    (K, L),  # Kayne and Landon
    (K, N),  # Kayne and Novetzke
    (L, O)   # Landon and Ong
]

# Check each answer choice
answer_index_list = []
for idx, (c1, c2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert that exactly candidates c1 and c2 are NOT assigned
    # (i.e., their total assignments = 0) and the other three are assigned exactly once
    # Since we already enforce each country gets one ambassador (total 3 assignments),
    # ensuring c1 and c2 have zero assignments implies the other three are assigned.
    
    # Ensure candidate c1 is not assigned to any country
    for c in range(3):
        s_chk.add(Not(assigned[c][c1]))
    
    # Ensure candidate c2 is not assigned to any country
    for c in range(3):
        s_chk.add(Not(assigned[c][c2]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)