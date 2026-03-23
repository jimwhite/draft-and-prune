from z3 import *

# Photographer indices: Frost=0, Gonzalez=1, Heideck=2, Knutson=3, Lai=4, Mays=5
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]
S = [Bool(f"S_{i}") for i in range(6)]  # S[i] is True if photographer i assigned to Silva

# Base solver
solver = Solver()

# At-least-two-per-ceremony constraints
# Silva has at least 2: sum of S[i] >= 2
solver.add(Sum([If(S[i], 1, 0) for i in range(6)]) >= 2)
# Thorne has at least 2: sum of (1 - S[i]) >= 2
solver.add(Sum([If(Not(S[i]), 1, 0) for i in range(6)]) >= 2)

# Frost-Heideck together constraint: S[0] == S[2]
solver.add(S[0] == S[2])

# Lai-Mays separation constraint: cannot both be assigned to same ceremony
solver.add(Or(Not(S[4]), Not(S[5])))

# Gonzalez conditional: If Gonzalez assigned to Silva, then Lai must be assigned to Thorne (i.e., not Silva)
solver.add(Implies(S[1], Not(S[4])))

# Knutson conditional: If Knutson not assigned to Thorne (i.e., assigned to Silva), then Heideck and Mays must be assigned to Thorne
# "If Knutson is not assigned to Thorne" means S[3] == True (assigned to Silva)
# Then both Heideck and Mays must be assigned to Thorne: S[2] == False, S[5] == False
solver.add(Implies(S[3], And(Not(S[2]), Not(S[5]))))

# Answer choices
answer_choices = [
    # Silva: Gonzalez, Lai; Thorne: Frost, Heideck, Mays
    {"Silva": ["Gonzalez", "Lai"], "Thorne": ["Frost", "Heideck", "Mays"]},
    # Silva: Gonzalez, Mays; Thorne: Knutson, Lai
    {"Silva": ["Gonzalez", "Mays"], "Thorne": ["Knutson", "Lai"]},
    # Silva: Frost, Gonzalez, Heideck; Thorne: Knutson, Lai, Mays
    {"Silva": ["Frost", "Gonzalez", "Heideck"], "Thorne": ["Knutson", "Lai", "Mays"]},
    # Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Lai
    {"Silva": ["Frost", "Heideck", "Mays"], "Thorne": ["Gonzalez", "Lai"]},
    # Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Knutson, Lai
    {"Silva": ["Frost", "Heideck", "Mays"], "Thorne": ["Gonzalez", "Knutson", "Lai"]}
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Build assignment based on choice
    for i, name in enumerate(photographers):
        if name in choice["Silva"]:
            s_chk.add(S[i] == True)
        elif name in choice["Thorne"]:
            s_chk.add(S[i] == False)
        else:
            # Not assigned to either ceremony
            s_chk.add(And(Not(S[i]), True))  # Explicitly not assigned to Silva (so Thorne or unassigned)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Print the index of the first acceptable assignment (as per question format)
if answer_index_list:
    print(answer_index_list[0])
else:
    print(-1)