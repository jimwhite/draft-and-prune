from z3 import *

# Photographer indices: Frost=0, Gonzalez=1, Heideck=2, Knutson=3, Lai=4, Mays=5
S = [Bool(f"S_{i}") for i in range(6)]  # Silva assignments
T = [Bool(f"T_{i}") for i in range(6)]  # Thorne assignments

solver = Solver()

# Mutual exclusivity: each photographer assigned to at most one ceremony
for i in range(6):
    solver.add(S[i] == Not(T[i]))

# Minimum assignment constraints: at least two per ceremony
solver.add(AtLeast(S[0], S[1], S[2], S[3], S[4], S[5], 2))
solver.add(AtLeast(T[0], T[1], T[2], T[3], T[4], T[5], 2))

# Frost-Heideck together constraint: S[0] == S[2]
solver.add(S[0] == S[2])

# Lai-Mays separation: cannot both be at Silva (T version is redundant due to mutual exclusivity)
solver.add(Not(And(S[4], S[5])))

# Gonzalez -> Lai implication: If Gonzalez at Silva, then Lai at Thorne
solver.add(Or(Not(S[1]), T[4]))

# Knutson conditional: If Knutson not at Thorne, then Heideck and Mays must be at Thorne
solver.add(Implies(Not(T[3]), And(T[2], T[5])))

# Answer choices
answer_choices = [
    ("Silva: Gonzalez, Lai; Thorne: Frost, Heideck, Mays", [1, 4], [0, 2, 5]),
    ("Silva: Gonzalez, Mays; Thorne: Knutson, Lai", [1, 5], [3, 4]),
    ("Silva: Frost, Gonzalez, Heideck; Thorne: Knutson, Lai, Mays", [0, 1, 2], [3, 4, 5]),
    ("Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Lai", [0, 2, 5], [1, 4]),
    ("Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Knutson, Lai", [0, 2, 5], [1, 3, 4])
]

# Check each answer choice
acceptable_indices = []
for idx, (desc, silva_ids, thorne_ids) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add concrete assignment constraints
    for i in range(6):
        if i in silva_ids:
            s_chk.add(S[i] == True, T[i] == False)
        elif i in thorne_ids:
            s_chk.add(S[i] == False, T[i] == True)
        else:
            # Not assigned to either ceremony
            s_chk.add(S[i] == False, T[i] == False)
    
    if s_chk.check() == sat:
        acceptable_indices.append(idx)

print(acceptable_indices)