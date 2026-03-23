from z3 import *

# Photographer indices: Frost=0, Gonzalez=1, Heideck=2, Knutson=3, Lai=4, Mays=5
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]

# assigned[i][c] = True if photographer i is assigned to ceremony c (0=Silva, 1=Thorne)
assigned = [[Bool(f"assigned_{i}_{c}") for c in range(2)] for i in range(6)]

solver = Solver()

# Non-overlap constraint: each photographer assigned to at most one ceremony
for i in range(6):
    solver.add(Or(And(assigned[i][0], Not(assigned[i][1])),
                  And(Not(assigned[i][0]), assigned[i][1]),
                  And(Not(assigned[i][0]), Not(assigned[i][1]))))

# Minimum assignment constraint: at least two photographers per ceremony
solver.add(Sum([If(assigned[i][0], 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(assigned[i][1], 1, 0) for i in range(6)]) >= 2)

# Frost–Heideck constraint: must be assigned together to the same ceremony
solver.add(assigned[0][0] == assigned[2][0])

# Lai–Mays separation constraint: cannot both be at the same ceremony
solver.add(Or(Not(assigned[4][0]), Not(assigned[5][0])))
solver.add(Or(Not(assigned[4][1]), Not(assigned[5][1])))

# Gonzalez–Lai implication: If Gonzalez at Silva, then Lai at Thorne
solver.add(Implies(assigned[1][0], assigned[4][1]))

# Knutson–conditional constraint: If Knutson not at Thorne, then Heideck and Mays must be at Thorne
solver.add(Implies(Not(assigned[3][1]), And(assigned[2][1], assigned[5][1])))

# Answer choices parsing
choices = [
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

answer_index_list = []

for idx, (desc, parts) in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add assignments for this choice
    for ph in parts["Silva"]:
        i = photographers.index(ph)
        s_chk.add(assigned[i][0])
    for ph in parts["Thorne"]:
        i = photographers.index(ph)
        s_chk.add(assigned[i][1])
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list[0])