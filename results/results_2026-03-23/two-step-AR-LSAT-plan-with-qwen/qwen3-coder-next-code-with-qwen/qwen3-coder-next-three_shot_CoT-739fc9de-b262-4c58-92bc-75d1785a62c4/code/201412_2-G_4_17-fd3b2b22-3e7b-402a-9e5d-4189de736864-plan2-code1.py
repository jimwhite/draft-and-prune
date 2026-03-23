from z3 import *

# Photographer indices: Frost=0, Gonzalez=1, Heideck=2, Knutson=3, Lai=4, Mays=5
S = [Bool(f"S_{i}") for i in range(6)]  # Silva assignments
T = [Bool(f"T_{i}") for i in range(6)]  # Thorne assignments

solver = Solver()

# Mutual exclusivity: no photographer assigned to both ceremonies
for i in range(6):
    solver.add(Not(And(S[i], T[i])))

# Minimum assignment constraint: at least two photographers at each ceremony
solver.add(Sum([If(S[i], 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(T[i], 1, 0) for i in range(6)]) >= 2)

# Frost-Heideck constraint: must be assigned together to one ceremony
solver.add(S[0] == S[2])  # Frost and Heideck same at Silva
solver.add(T[0] == T[2])  # Frost and Heideck same at Thorne
solver.add(Or(S[0], S[2]))  # At least one of them assigned (ensures both are assigned to same ceremony)

# Lai-Mays constraint: if both assigned, must be at different ceremonies
solver.add(Not(And(S[4], S[5])))  # Not both at Silva
solver.add(Not(And(T[4], T[5])))  # Not both at Thorne

# Gonzalez->Lai constraint: If Gonzalez is at Silva, then Lai must be at Thorne
solver.add(Implies(S[1], T[4]))

# Knutson conditional constraint: If Knutson is not at Thorne, then both Heideck and Mays must be at Thorne
solver.add(Implies(Not(T[3]), And(T[2], T[5])))

# Answer choices
answer_choices = [
    {"Silva": ["Gonzalez", "Lai"], "Thorne": ["Frost", "Heideck", "Mays"]},
    {"Silva": ["Gonzalez", "Mays"], "Thorne": ["Knutson", "Lai"]},
    {"Silva": ["Frost", "Gonzalez", "Heideck"], "Thorne": ["Knutson", "Lai", "Mays"]},
    {"Silva": ["Frost", "Heideck", "Mays"], "Thorne": ["Gonzalez", "Lai"]},
    {"Silva": ["Frost", "Heideck", "Mays"], "Thorne": ["Gonzalez", "Knutson", "Lai"]}
]

# Photographer name to index mapping
name_to_idx = {"Frost": 0, "Gonzalez": 1, "Heideck": 2, "Knutson": 3, "Lai": 4, "Mays": 5}

# Check each answer choice
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Set assignments based on the choice
    for i in range(6):
        name = list(name_to_idx.keys())[i]
        s_chk.add(S[i] == (name in choice["Silva"]))
        s_chk.add(T[i] == (name in choice["Thorne"]))
    
    if s_chk.check() == sat:
        print(idx)
        break