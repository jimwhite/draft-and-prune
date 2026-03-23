from z3 import *

# Photographer indices
(FROST, GONZ, HEID, KNUT, LAI, MAYS) = range(6)

# S[i] = True if photographer i assigned to Silva, False for Thorne
S = [Bool(f"S_{i}") for i in range(6)]

# Base solver
solver = Solver()

# At-least-two-per-ceremony constraints
## Silva: at least 2 photographers
solver.add(Sum([If(S[i], 1, 0) for i in range(6)]) >= 2)
## Thorne: at least 2 photographers
solver.add(Sum([If(Not(S[i]), 1, 0) for i in range(6)]) >= 2)

# Frost–Heideck together constraint
solver.add(S[FROST] == S[HEID])

# Lai–Mays separation constraint: if both assigned, they must be on different ceremonies
solver.add(Or(Not(S[LAI]), Not(S[MAYS]), S[LAI] != S[MAYS]))

# Gonzalez → Lai conditional: If Gonzalez is at Silva, then Lai must be at Thorne
solver.add(Implies(S[GONZ], Not(S[LAI])))

# Knutson conditional: If Knutson is not at Thorne (i.e., at Silva), then both Heideck and Mays must be at Thorne
solver.add(Implies(S[KNUT], And(Not(S[HEID]), Not(S[MAYS]))))

# Answer choices
choices = [
    # Silva: Gonzalez, Lai; Thorne: Frost, Heideck, Mays
    # S[GONZ]=True, S[LAI]=True, S[FROST]=False, S[HEID]=False, S[MAYS]=False
    # Others (KNUT) can be assigned arbitrarily but must satisfy constraints
    [GONZ, LAI],  # Silva photographers
    
    # Silva: Gonzalez, Mays; Thorne: Knutson, Lai
    [GONZ, MAYS],
    
    # Silva: Frost, Gonzalez, Heideck; Thorne: Knutson, Lai, Mays
    [FROST, GONZ, HEID],
    
    # Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Lai
    [FROST, HEID, MAYS],
    
    # Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Knutson, Lai
    [FROST, HEID, MAYS]
]

# Check each choice
answer_index_list = []
for idx, Silva_photographers in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Build assignment for this choice
    Silva_set = set(Silva_photographers)
    
    # Assign photographers to ceremonies according to the choice
    for i in range(6):
        if i in Silva_set:
            s_chk.add(S[i] == True)
        else:
            s_chk.add(S[i] == False)
    
    # Check satisfiability
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)