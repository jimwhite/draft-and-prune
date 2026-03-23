from z3 import *

# Photographer indices: 0:Frost, 1:Gonzalez, 2:Heideck, 3:Knutson, 4:Lai, 5:Mays
S = [Bool(f"S_{i}") for i in range(6)]  # Silva assignments
T = [Bool(f"T_{i}") for i in range(6)]  # Thorne assignments

solver = Solver()

# Mutual exclusivity: each photographer assigned to at most one ceremony
for i in range(6):
    solver.add(Or(And(S[i], Not(T[i])), And(Not(S[i]), T[i]), And(Not(S[i]), Not(T[i]))))

# At least two photographers per ceremony
solver.add(Sum([If(S[i], 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(T[i], 1, 0) for i in range(6)]) >= 2)

# Frost and Heideck must be assigned together to the same ceremony
solver.add(S[0] == S[2])

# If Lai and Mays are both assigned, they must be on different ceremonies
solver.add(Or(Not(S[4]), Not(S[5]), Not(T[4]), Not(T[5]), S[4] != S[5]))

# If Gonzalez is on Silva, then Lai must be on Thorne
solver.add(Implies(S[1], T[4]))

# If Knutson is not on Thorne, then both Heideck and Mays must be on Thorne
# Equivalent: If Knutson is not on Thorne (i.e., S[3] or unassigned), then Heideck and Mays must be on Thorne
# Using T[i] = Not(S[i]) for assigned photographers, but since we allow unassigned, better to express directly:
# Knutson not on Thorne => Heideck and Mays on Thorne
solver.add(Implies(Not(T[3]), And(T[2], T[5])))

# Answer choices
answer_choices = [
    ("Silva University: Gonzalez, Lai Thorne University: Frost, Heideck, Mays",
     {"Silva": ["Gonzalez", "Lai"], "Thorne": ["Frost", "Heideck", "Mays"]}),
    ("Silva University: Gonzalez, Mays Thorne University: Knutson, Lai",
     {"Silva": ["Gonzalez", "Mays"], "Thorne": ["Knutson", "Lai"]}),
    ("Silva University: Frost, Gonzalez, Heideck Thorne University: Knutson, Lai, Mays",
     {"Silva": ["Frost", "Gonzalez", "Heideck"], "Thorne": ["Knutson", "Lai", "Mays"]}),
    ("Silva University: Frost, Heideck, Mays Thorne University: Gonzalez, Lai",
     {"Silva": ["Frost", "Heideck", "Mays"], "Thorne": ["Gonzalez", "Lai"]}),
    ("Silva University: Frost, Heideck, Mays Thorne University: Gonzalez, Knutson, Lai",
     {"Silva": ["Frost", "Heideck", "Mays"], "Thorne": ["Gonzalez", "Knutson", "Lai"]})
]

# Map names to indices
name_to_idx = {
    "Frost": 0, "Gonzalez": 1, "Heideck": 2,
    "Knutson": 3, "Lai": 4, "Mays": 5
}

# Check each answer choice
satisfiable_indices = []
for idx, (desc, assignment) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Initialize all assignments as unassigned (False for both)
    s_S = [False] * 6
    s_T = [False] * 6
    
    # Process Silva assignments
    for name in assignment["Silva"]:
        i = name_to_idx[name]
        s_S[i] = True
    
    # Process Thorne assignments
    for name in assignment["Thorne"]:
        i = name_to_idx[name]
        s_T[i] = True
    
    # Add constraints for this assignment
    for i in range(6):
        if s_S[i]:
            s_chk.add(S[i])
        else:
            s_chk.add(Not(S[i]))
        
        if s_T[i]:
            s_chk.add(T[i])
        else:
            s_chk.add(Not(T[i]))
    
    # Check satisfiability
    if s_chk.check() == sat:
        satisfiable_indices.append(idx)

# Output the index of the first (and only) acceptable assignment
if satisfiable_indices:
    print(satisfiable_indices[0])
else:
    print(-1)