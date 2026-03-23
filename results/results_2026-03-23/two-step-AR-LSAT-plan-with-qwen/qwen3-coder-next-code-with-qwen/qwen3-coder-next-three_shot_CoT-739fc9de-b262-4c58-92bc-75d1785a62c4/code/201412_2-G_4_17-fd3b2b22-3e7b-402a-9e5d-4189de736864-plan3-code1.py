from z3 import *

# Photographer indices: Frost=0, Gonzalez=1, Heideck=2, Knutson=3, Lai=4, Mays=5
S = [Bool(f"S_{i}") for i in range(6)]  # Silva assignment
T = [Bool(f"T_{i}") for i in range(6)]  # Thorne assignment

solver = Solver()

# Mutual exclusivity: no photographer assigned to both ceremonies
for i in range(6):
    solver.add(Not(And(S[i], T[i])))

# At least two photographers per ceremony
solver.add(Sum([If(S[i], 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(T[i], 1, 0) for i in range(6)]) >= 2)

# Frost (0) and Heideck (2) must be assigned together to one ceremony
solver.add(S[0] == S[2])
solver.add(T[0] == T[2])
# They must be assigned (at least one is assigned → both are)
solver.add(Or(S[0], T[0]))

# If Lai (4) and Mays (5) are both assigned, they must be on different ceremonies
# A[i] = S[i] | T[i]
solver.add(Or(Not(S[4] | T[4]), Not(S[5] | T[5]), S[4] != S[5]))

# If Gonzalez (1) is assigned to Silva, then Lai must be assigned to Thorne
# S[1] → T[4]
solver.add(Implies(S[1], T[4]))

# If Knutson (3) is not assigned to Thorne, then Heideck (2) and Mays (5) must be assigned to Thorne
# ~T[3] → (T[2] & T[5])
solver.add(Implies(Not(T[3]), And(T[2], T[5])))

# Answer choices
choices = [
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

# Check each choice
valid_indices = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Fix assignments for this choice
    all_assigned = set(choice["Silva"]) | set(choice["Thorne"])
    
    for i in range(6):
        if i in choice["Silva"]:
            s_chk.add(S[i] == True, T[i] == False)
        elif i in choice["Thorne"]:
            s_chk.add(S[i] == False, T[i] == True)
        else:
            # Not assigned to either ceremony
            s_chk.add(S[i] == False, T[i] == False)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)