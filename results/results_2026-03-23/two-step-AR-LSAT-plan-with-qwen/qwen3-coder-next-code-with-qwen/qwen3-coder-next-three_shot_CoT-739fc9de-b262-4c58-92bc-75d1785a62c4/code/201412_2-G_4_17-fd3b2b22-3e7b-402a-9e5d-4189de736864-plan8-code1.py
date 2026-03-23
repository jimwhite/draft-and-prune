from z3 import *

# Photographer indices: 0=Frost, 1=Gonzalez, 2=Heideck, 3=Knutson, 4=Lai, 5=Mays
S = [Bool(f"S_{i}") for i in range(6)]
T = [Bool(f"T_{i}") for i in range(6)]

solver = Solver()

# Mutual exclusion: no photographer assigned to both ceremonies
for i in range(6):
    solver.add(Not(And(S[i], T[i])))

# At least two photographers per ceremony
solver.add(Sum([If(S[i], 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(T[i], 1, 0) for i in range(6)]) >= 2)

# Frost and Heideck must be assigned together to the same ceremony
solver.add(S[0] == S[2])
solver.add(T[0] == T[2])

# Lai and Mays: if both are assigned, they must be on different ceremonies
solver.add(Implies(
    And(S[4] + T[4] == 1, S[5] + T[5] == 1),
    S[4] != S[5]
))

# If Gonzalez is at Silva, then Lai must be at Thorne
solver.add(Implies(S[1], T[4]))

# If Knutson is not at Thorne, then both Heideck and Mays must be at Thorne
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
for idx, (desc, assignment) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Set assignments for this choice
    for ceremony, photographers in assignment.items():
        for name in photographers:
            i = name_to_idx[name]
            if ceremony == "Silva":
                s_chk.add(S[i])
            else:  # Thorne
                s_chk.add(T[i])
    
    if s_chk.check() == sat:
        print(idx)
        break