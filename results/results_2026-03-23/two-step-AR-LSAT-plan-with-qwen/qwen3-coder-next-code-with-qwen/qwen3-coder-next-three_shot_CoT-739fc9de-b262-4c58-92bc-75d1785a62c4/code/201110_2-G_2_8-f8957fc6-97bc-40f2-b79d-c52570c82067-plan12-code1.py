from z3 import *

# Candidate indices: Jaramillo=0, Kayne=1, Landon=2, Novetzke=3, Ong=4
CANDIDATES = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]
(J, K, L, N, O) = range(5)

# Assignment variables: v_en (Venezuela), y_en (Yemen), z_en (Zambia)
v_en = Int("v_en")
y_en = Int("y_en")
z_en = Int("z_en")

# Base solver
solver = Solver()

# Distinctness constraint: all ambassadors are different people
solver.add(Distinct(v_en, y_en, z_en))

# Constraint 1: Exactly one of Kayne or Novetzke is assigned
k_assigned = Or(v_en == K, y_en == K, z_en == K)
n_assigned = Or(v_en == N, y_en == N, z_en == N)
solver.add(Xor(k_assigned, n_assigned))

# Constraint 2: If Jaramillo is assigned, then Kayne must be assigned
j_assigned = Or(v_en == J, y_en == J, z_en == J)
solver.add(Implies(j_assigned, k_assigned))

# Constraint 3: If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
solver.add(Implies(v_en == O, y_en != K))

# Constraint 4: If Landon is assigned, it must be to Zambia
l_assigned = Or(v_en == L, y_en == L, z_en == L)
solver.add(Implies(l_assigned, z_en == L))

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
for idx, (a, b) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert that candidates a and b are NOT assigned (i.e., not in any of the three positions)
    s_chk.add(And(
        v_en != a, v_en != b,
        y_en != a, y_en != b,
        z_en != a, z_en != b
    ))
    
    # If SAT, this pair could be unassigned
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)