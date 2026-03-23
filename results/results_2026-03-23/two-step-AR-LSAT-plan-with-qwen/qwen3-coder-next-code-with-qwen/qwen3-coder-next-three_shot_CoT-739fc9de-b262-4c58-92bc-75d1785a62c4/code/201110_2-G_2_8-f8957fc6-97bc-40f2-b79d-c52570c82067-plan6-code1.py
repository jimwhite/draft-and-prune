from z3 import *

# Candidate indices: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
CANDIDATES = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]
J, K, L, N, O = 0, 1, 2, 3, 4

# Boolean variables for assignment
assigned = [Bool(f"assigned_{i}") for i in range(5)]

# Country assignment variables: to_country[i] = which country candidate i is assigned to
# 0=Venezuela, 1=Yemen, 2=Zambia, -1=unassigned
to_country = [Int(f"to_country_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Each candidate assigned to exactly one country or unassigned
for i in range(5):
    solver.add(Or(to_country[i] == -1, to_country[i] == 0, to_country[i] == 1, to_country[i] == 2))

# Consistency between assigned and to_country
for i in range(5):
    solver.add(assigned[i] == (to_country[i] != -1))

# Exactly 3 ambassadors assigned (one per country)
solver.add(Sum([If(assigned[i], 1, 0) for i in range(5)]) == 3)

# Exactly one candidate per country
for c in range(3):
    candidates_for_country = [to_country[i] == c for i in range(5)]
    solver.add(PbAtLeast(candidates_for_country, 1))
    solver.add(PbAtMost(candidates_for_country, 1))

# Exclusive Kayne/Novetzke constraint (XOR)
solver.add(assigned[K] != assigned[N])

# Jaramillo → Kayne constraint
solver.add(Implies(assigned[J], assigned[K]))

# If Ong is assigned to Venezuela, then Kayne must not be assigned to Yemen
solver.add(Implies(to_country[O] == 0, Not(to_country[K] == 1)))

# Landon constraint: If assigned, must be to Zambia
solver.add(Implies(assigned[L], to_country[L] == 2))

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
    
    # Assert that only c1 and c2 are unassigned
    for i in range(5):
        if i == c1 or i == c2:
            s_chk.add(Not(assigned[i]))
        else:
            s_chk.add(assigned[i])
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)