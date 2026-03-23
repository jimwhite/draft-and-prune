from z3 import *

# Photographer indices: 0-Frost, 1-Gonzalez, 2-Heideck, 3-Knutson, 4-Lai, 5-Mays
PHOTOGRAPHERS = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]
n = len(PHOTOGRAPHERS)

# S[i] = True if photographer i assigned to Silva
# T[i] = True if photographer i assigned to Thorne
S = [Bool(f"S_{i}") for i in range(n)]
T = [Bool(f"T_{i}") for i in range(n)]

solver = Solver()

# Minimum capacity constraints: at least 2 per ceremony
solver.add(Sum([If(s, 1, 0) for s in S]) >= 2)
solver.add(Sum([If(t, 1, 0) for t in T]) >= 2)

# Mutual exclusivity: no photographer assigned to both ceremonies
for i in range(n):
    solver.add(Not(And(S[i], T[i])))

# Frost and Heideck must be assigned together to the same ceremony if assigned at all
# (S_Frost ↔ S_Heideck) ∧ (T_Frost ↔ T_Heideck)
solver.add(S[0] == S[2])
solver.add(T[0] == T[2])

# Lai and Mays: if both assigned, must be on different ceremonies
# Equivalent to: not (both Silva) and not (both Thorne)
solver.add(Not(And(S[4], S[5])))
solver.add(Not(And(T[4], T[5])))

# If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(S[1], T[4]))

# If Knutson is NOT assigned to Thorne, then Heideck and Mays must be assigned to Thorne
solver.add(Implies(Not(T[3]), And(T[2], T[5])))

# Answer choices
choices = [
    # Silva University: Gonzalez, Lai | Thorne University: Frost, Heideck, Mays
    {"Silva": ["Gonzalez", "Lai"], "Thorne": ["Frost", "Heideck", "Mays"]},
    # Silva University: Gonzalez, Mays | Thorne University: Knutson, Lai
    {"Silva": ["Gonzalez", "Mays"], "Thorne": ["Knutson", "Lai"]},
    # Silva University: Frost, Gonzalez, Heideck | Thorne University: Knutson, Lai, Mays
    {"Silva": ["Frost", "Gonzalez", "Heideck"], "Thorne": ["Knutson", "Lai", "Mays"]},
    # Silva University: Frost, Heideck, Mays | Thorne University: Gonzalez, Lai
    {"Silva": ["Frost", "Heideck", "Mays"], "Thorne": ["Gonzalez", "Lai"]},
    # Silva University: Frost, Heideck, Mays | Thorne University: Gonzalez, Knutson, Lai
    {"Silva": ["Frost", "Heideck", "Mays"], "Thorne": ["Gonzalez", "Knutson", "Lai"]}
]

# Map photographer names to indices
name_to_idx = {name: i for i, name in enumerate(PHOTOGRAPHERS)}

# Check each choice
answer_index_list = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    # Add base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add assignment constraints for this choice
    for name in choice["Silva"]:
        i = name_to_idx[name]
        s_chk.add(S[i])
    for name in choice["Thorne"]:
        i = name_to_idx[name]
        s_chk.add(T[i])
    
    # Unmentioned photographers are not assigned to either ceremony
    all_names = set(choice["Silva"] + choice["Thorne"])
    for name in PHOTOGRAPHERS:
        if name not in all_names:
            i = name_to_idx[name]
            s_chk.add(Not(S[i]), Not(T[i]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Output the index of acceptable assignment(s)
print(answer_index_list)