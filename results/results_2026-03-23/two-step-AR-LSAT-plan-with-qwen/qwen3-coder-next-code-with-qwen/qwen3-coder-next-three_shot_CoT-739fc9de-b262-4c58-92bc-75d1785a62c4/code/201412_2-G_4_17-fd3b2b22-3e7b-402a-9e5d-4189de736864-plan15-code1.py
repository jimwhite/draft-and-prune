from z3 import *

# Photographer indices: 0-Frost, 1-Gonzalez, 2-Heideck, 3-Knutson, 4-Lai, 5-Mays
(FROST, GONZ, HEID, KNUT, LAI, MAYS) = range(6)

# Boolean variables: S[i] = photographer i assigned to Silva, T[i] = photographer i assigned to Thorne
S = [Bool(f"S_{i}") for i in range(6)]
T = [Bool(f"T_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Mutual exclusivity: each photographer can be assigned to at most one ceremony (or none)
for i in range(6):
    solver.add(Not(And(S[i], T[i])))

# At-least-two constraint: at least two photographers assigned to each ceremony
solver.add(Sum([If(S[i], 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(T[i], 1, 0) for i in range(6)]) >= 2)

# Frost-Heideck together constraint: both assigned to same ceremony (both S or both T)
solver.add(S[FROST] == S[HEID])
solver.add(T[FROST] == T[HEID])

# Lai-Mays separation constraint: if both assigned, they must be at different ceremonies
solver.add(Not(And(S[LAI], S[MAYS])))
solver.add(Not(And(T[LAI], T[MAYS])))

# Gonzalez → Lai conditional: if Gonzalez at Silva, then Lai must be at Thorne
solver.add(Implies(S[GONZ], T[LAI]))

# Knutson conditional: if Knutson NOT at Thorne, then Heideck and Mays must be at Thorne
solver.add(Implies(Not(T[KNUT]), And(T[HEID], T[MAYS])))

# Answer choices
answer_choices = [
    # 0: Silva: Gonzalez, Lai; Thorne: Frost, Heideck, Mays
    {"Silva": [GONZ, LAI], "Thorne": [FROST, HEID, MAYS]},
    # 1: Silva: Gonzalez, Mays; Thorne: Knutson, Lai
    {"Silva": [GONZ, MAYS], "Thorne": [KNUT, LAI]},
    # 2: Silva: Frost, Gonzalez, Heideck; Thorne: Knutson, Lai, Mays
    {"Silva": [FROST, GONZ, HEID], "Thorne": [KNUT, LAI, MAYS]},
    # 3: Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Lai
    {"Silva": [FROST, HEID, MAYS], "Thorne": [GONZ, LAI]},
    # 4: Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Knutson, Lai
    {"Silva": [FROST, HEID, MAYS], "Thorne": [GONZ, KNUT, LAI]}
]

# Check each answer choice
acceptable_indices = []
for idx, assignment in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Build explicit assignment constraints
    assigned = set(assignment["Silva"] + assignment["Thorne"])
    
    # For each photographer
    for i in range(6):
        if i in assignment["Silva"]:
            s_chk.add(S[i], Not(T[i]))
        elif i in assignment["Thorne"]:
            s_chk.add(Not(S[i]), T[i])
        else:
            # Not assigned to either ceremony
            s_chk.add(Not(S[i]), Not(T[i]))
    
    if s_chk.check() == sat:
        acceptable_indices.append(idx)

print(acceptable_indices)