from z3 import *

# Candidate indices: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
# Country indices: 0=Venezuela, 1=Yemen, 2=Zambia

# Assignment variables: c_ven, c_yem, c_zam for each candidate c
J = [Bool(f"J_{c}") for c in ["ven", "yem", "zam"]]
K = [Bool(f"K_{c}") for c in ["ven", "yem", "zam"]]
L = [Bool(f"L_{c}") for c in ["ven", "yem", "zam"]]
N = [Bool(f"N_{c}") for c in ["ven", "yem", "zam"]]
O = [Bool(f"O_{c}") for c in ["ven", "yem", "zam"]]

# Base solver
solver = Solver()

# Exactly-one-country-per-ambassador: each candidate assigned to at most one country
for cand in [J, K, L, N, O]:
    solver.add(PbLe([(c, 1) for c in cand], 1))

# Exactly-one-ambassador-per-country: each country has exactly one ambassador
for country_idx in range(3):
    solver.add(Sum([J[country_idx], K[country_idx], L[country_idx], N[country_idx], O[country_idx]]) == 1)

# Exactly two candidates are unassigned (i.e., exactly three assigned)
total_assigned = Sum([If(c, 1, 0) for cand in [J, K, L, N, O] for c in cand])
solver.add(total_assigned == 3)

# Exclusive Kayne/Novetzke: exactly one of them is assigned to any country
k_any = Or(*K)
n_any = Or(*N)
solver.add(Xor(k_any, n_any))

# Jaramillo ⇒ Kayne: if Jaramillo is assigned to any country, then Kayne must be assigned
solver.add(Implies(Or(*J), Or(*K)))

# Ong→Venezuela ⇒ ¬Kayne→Yemen: if Ong is assigned to Venezuela, then Kayne cannot be assigned to Yemen
solver.add(Implies(O[0], Not(K[1])))

# Landon ⇒ Zambia: if Landon is assigned, it must be to Zambia
solver.add(Not(L[0]))  # Landon not assigned to Venezuela
solver.add(Not(L[1]))  # Landon not assigned to Yemen

# Answer choices: pairs of candidates who are NOT assigned
answer_choices = [
    (0, 3),  # Jaramillo and Novetzke
    (0, 4),  # Jaramillo and Ong
    (1, 2),  # Kayne and Landon
    (1, 3),  # Kayne and Novetzke
    (2, 4)   # Landon and Ong
]

# Check each answer choice
answer_index_list = []
for idx, (c1, c2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Set the two candidates to be unassigned (all their assignment variables false)
    if c1 == 0:
        s_chk.add(Not(J[0]), Not(J[1]), Not(J[2]))
    elif c1 == 1:
        s_chk.add(Not(K[0]), Not(K[1]), Not(K[2]))
    elif c1 == 2:
        s_chk.add(Not(L[0]), Not(L[1]), Not(L[2]))
    elif c1 == 3:
        s_chk.add(Not(N[0]), Not(N[1]), Not(N[2]))
    elif c1 == 4:
        s_chk.add(Not(O[0]), Not(O[1]), Not(O[2]))
    
    if c2 == 0:
        s_chk.add(Not(J[0]), Not(J[1]), Not(J[2]))
    elif c2 == 1:
        s_chk.add(Not(K[0]), Not(K[1]), Not(K[2]))
    elif c2 == 2:
        s_chk.add(Not(L[0]), Not(L[1]), Not(L[2]))
    elif c2 == 3:
        s_chk.add(Not(N[0]), Not(N[1]), Not(N[2]))
    elif c2 == 4:
        s_chk.add(Not(O[0]), Not(O[1]), Not(O[2]))
    
    # Ensure the remaining three candidates are each assigned to exactly one country
    remaining = [i for i in range(5) if i != c1 and i != c2]
    for r in remaining:
        if r == 0:  # Jaramillo
            s_chk.add(Or(J[0], J[1], J[2]))
        elif r == 1:  # Kayne
            s_chk.add(Or(K[0], K[1], K[2]))
        elif r == 2:  # Landon
            s_chk.add(Or(L[0], L[1], L[2]))
        elif r == 3:  # Novetzke
            s_chk.add(Or(N[0], N[1], N[2]))
        elif r == 4:  # Ong
            s_chk.add(Or(O[0], O[1], O[2]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)