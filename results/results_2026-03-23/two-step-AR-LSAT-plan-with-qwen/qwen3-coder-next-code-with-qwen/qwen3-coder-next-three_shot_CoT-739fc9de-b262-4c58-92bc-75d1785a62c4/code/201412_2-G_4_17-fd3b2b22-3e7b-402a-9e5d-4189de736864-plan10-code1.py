from z3 import *

# Photographer indices: 0-Frost, 1-Gonzalez, 2-Heideck, 3-Knutson, 4-Lai, 5-Mays
s = [Bool(f"s_{i}") for i in range(6)]  # Silva assignments
t = [Bool(f"t_{i}") for i in range(6)]  # Thorne assignments

# Base solver
solver = Solver()

# Mutual exclusivity: no photographer assigned to both ceremonies
for i in range(6):
    solver.add(Not(And(s[i], t[i])))

# At least two photographers per ceremony
solver.add(Sum([If(s[i], 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(t[i], 1, 0) for i in range(6)]) >= 2)

# Frost and Heideck must be assigned together to the same ceremony
solver.add(s[0] == s[2])

# If Lai and Mays are both assigned, they must be at different ceremonies
solver.add(Not(And(s[4], s[5])))
solver.add(Not(And(t[4], t[5])))

# If Gonzalez is assigned to Silva, then Lai must be at Thorne
solver.add(Or(Not(s[1]), t[4]))

# If Knutson is not at Thorne, then Heideck and Mays must be at Thorne
solver.add(Or(t[3], And(t[2], t[5])))

# Answer choices
answer_choices = [
    {"Silva": [1, 4], "Thorne": [0, 2, 5]},      # Gonzalez, Lai | Frost, Heideck, Mays
    {"Silva": [1, 5], "Thorne": [3, 4]},         # Gonzalez, Mays | Knutson, Lai
    {"Silva": [0, 1, 2], "Thorne": [3, 4, 5]},   # Frost, Gonzalez, Heideck | Knutson, Lai, Mays
    {"Silva": [0, 2, 5], "Thorne": [1, 4]},      # Frost, Heideck, Mays | Gonzalez, Lai
    {"Silva": [0, 2, 5], "Thorne": [1, 3, 4]}    # Frost, Heideck, Mays | Gonzalez, Knutson, Lai
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Set assignments based on the choice
    for i in range(6):
        s_chk.add(s[i] == (i in choice["Silva"]))
        s_chk.add(t[i] == (i in choice["Thorne"]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)