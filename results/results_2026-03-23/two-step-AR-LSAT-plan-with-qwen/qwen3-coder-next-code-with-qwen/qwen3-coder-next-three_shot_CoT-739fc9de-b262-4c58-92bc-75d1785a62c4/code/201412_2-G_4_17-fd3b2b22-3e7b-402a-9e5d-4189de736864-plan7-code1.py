from z3 import *

# Photographer indices: Frost=0, Gonzalez=1, Heideck=2, Knutson=3, Lai=4, Mays=5
S = [Bool(f"S_{i}") for i in range(6)]  # Silva assignment
T = [Bool(f"T_{i}") for i in range(6)]  # Thorne assignment

solver = Solver()

# Non-crossing constraint: each photographer assigned to at most one ceremony
for i in range(6):
    solver.add(Not(And(S[i], T[i])))

# Minimum assignment constraint: at least two photographers per ceremony
solver.add(Sum([If(S[i], 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(T[i], 1, 0) for i in range(6)]) >= 2)

# Frost–Heideck together constraint: assigned to same ceremony (or both unassigned)
solver.add(S[0] == S[2])
solver.add(T[0] == T[2])

# Lai–Mays separation constraint: not both at same ceremony
solver.add(Or(Not(S[4]), Not(S[5])))
solver.add(Or(Not(T[4]), Not(T[5])))

# Gonzalez → Lai conditional: If Gonzalez at Silva, then Lai must be at Thorne
solver.add(Implies(S[1], T[4]))

# Knutson conditional: If Knutson not at Thorne, then Heideck and Mays must be at Thorne
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
    "Frost": 0,
    "Gonzalez": 1,
    "Heideck": 2,
    "Knutson": 3,
    "Lai": 4,
    "Mays": 5
}

# Check each answer choice
answer_index_list = []
for idx, (desc, assignment) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints based on the assignment
    for ceremony, photographers in assignment.items():
        for photographer in photographers:
            i = name_to_idx[photographer]
            if ceremony == "Silva":
                s_chk.add(S[i] == True)
                s_chk.add(T[i] == False)
            else:  # Thorne
                s_chk.add(S[i] == False)
                s_chk.add(T[i] == True)
    
    # For photographers not mentioned, they are unassigned
    all_photographers = set(name_to_idx.keys())
    assigned_in_choice = set()
    for photographers in assignment.values():
        assigned_in_choice.update(photographers)
    
    for photographer in all_photographers - assigned_in_choice:
        i = name_to_idx[photographer]
        s_chk.add(S[i] == False)
        s_chk.add(T[i] == False)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)