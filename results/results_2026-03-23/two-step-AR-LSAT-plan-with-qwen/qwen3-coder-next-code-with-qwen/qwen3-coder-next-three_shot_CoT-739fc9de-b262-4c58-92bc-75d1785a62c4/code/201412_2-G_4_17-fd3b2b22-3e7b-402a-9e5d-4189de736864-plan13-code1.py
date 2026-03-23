from z3 import *

# Photographer indices: Frost=0, Gonzalez=1, Heideck=2, Knutson=3, Lai=4, Mays=5
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]

# Boolean variables: s[i] = photographer i assigned to Silva, t[i] = photographer i assigned to Thorne
s = [Bool(f"s_{i}") for i in range(6)]
t = [Bool(f"t_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Mutual exclusivity constraint: no photographer assigned to both ceremonies
for i in range(6):
    solver.add(Not(And(s[i], t[i])))

# At-least-two constraint: at least two photographers assigned to each ceremony
solver.add(Sum([If(s[i], 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(t[i], 1, 0) for i in range(6)]) >= 2)

# Frost-Heideck together constraint: both assigned to same ceremony
solver.add(s[0] == s[2])
solver.add(t[0] == t[2])

# Lai-Mays separation constraint: if both assigned, they must be on different ceremonies
solver.add(Not(And(s[4], s[5])))
solver.add(Not(And(t[4], t[5])))

# Gonzalez-Lai conditional constraint: if Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(s[1], t[4]))

# Knutson-conditional constraint: if Knutson is not assigned to Thorne, then Heideck and Mays must both be assigned to Thorne
solver.add(Implies(Not(t[3]), And(t[2], t[5])))

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
    
    # Add assertions for the specific assignment
    assigned_to_silva = set(choice["Silva"])
    assigned_to_thorne = set(choice["Thorne"])
    
    for i in range(6):
        if i in assigned_to_silva:
            s_chk.add(s[i], Not(t[i]))
        elif i in assigned_to_thorne:
            s_chk.add(Not(s[i]), t[i])
        else:
            # Not assigned to either ceremony
            s_chk.add(Not(s[i]), Not(t[i]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)