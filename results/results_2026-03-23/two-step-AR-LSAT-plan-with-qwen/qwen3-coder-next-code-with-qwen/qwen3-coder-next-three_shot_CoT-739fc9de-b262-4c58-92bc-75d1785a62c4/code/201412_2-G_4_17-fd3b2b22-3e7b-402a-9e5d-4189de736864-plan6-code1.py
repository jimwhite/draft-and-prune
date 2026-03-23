from z3 import *

# Photographer indices: 0-Frost, 1-Gonzalez, 2-Heideck, 3-Knutson, 4-Lai, 5-Mays
S = [Bool(f"S_{i}") for i in range(6)]  # Silva assignments
T = [Bool(f"T_{i}") for i in range(6)]  # Thorne assignments

solver = Solver()

# Mutual exclusivity: no photographer assigned to both ceremonies
for i in range(6):
    solver.add(Not(And(S[i], T[i])))

# At-least-two constraint per ceremony
solver.add(Sum([If(S[i], 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(T[i], 1, 0) for i in range(6)]) >= 2)

# Frost–Heideck together constraint: must be assigned to same ceremony and at least one of them is assigned
solver.add(S[0] == S[2])
solver.add(T[0] == T[2])
solver.add(Or(S[0], S[2]))

# Lai–Mays separation constraint: cannot both be at Silva or both at Thorne
solver.add(Not(And(S[4], S[5])))
solver.add(Not(And(T[4], T[5])))

# Gonzalez → Lai conditional: If Gonzalez is at Silva, then Lai must be at Thorne
solver.add(Or(Not(S[1]), T[4]))

# Knutson conditional: If Knutson is not at Thorne, then Heideck and Mays must be at Thorne
solver.add(Implies(Not(T[3]), And(T[2], T[5])))

# Answer choices
answer_choices = [
    # Silva: Gonzalez, Lai; Thorne: Frost, Heideck, Mays
    {"Silva": [1, 4], "Thorne": [0, 2, 5]},
    # Silva: Gonzalez, Mays; Thorne: Knutson, Lai
    {"Silva": [1, 5], "Thorne": [3, 4]},
    # Silva: Frost, Gonzalez, Heideck; Thorne: Knutson, Lai, Mays
    {"Silva": [0, 1, 2], "Thorne": [3, 4, 5]},
    # Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Lai
    {"Silva": [0, 2, 5], "Thorne": [1, 4]},
    # Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Knutson, Lai
    {"Silva": [0, 2, 5], "Thorne": [1, 3, 4]}
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Set assignments for this choice
    for i in range(6):
        if i in choice["Silva"]:
            s_chk.add(S[i])
        else:
            s_chk.add(Not(S[i]))
        if i in choice["Thorne"]:
            s_chk.add(T[i])
        else:
            s_chk.add(Not(T[i]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)