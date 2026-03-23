from z3 import *

# Candidate indices: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
# Country indices: 0=unassigned, 1=Venezuela, 2=Yemen, 3=Zambia

# Boolean variables: assigned[i] = True if candidate i is assigned
assigned = [Bool(f"assigned_{i}") for i in range(5)]

# Integer variables: amb[i] = country assigned to candidate i (0 if unassigned)
amb = [Int(f"amb_{i}") for i in range(5)]

solver = Solver()

# Exactly three candidates are assigned
solver.add(Sum([If(assigned[i], 1, 0) for i in range(5)]) == 3)

# One ambassador per country (Venezuela, Yemen, Zambia)
for c in [1, 2, 3]:
    # Exactly one candidate assigned to country c
    solver.add(Sum([If(amb[i] == c, 1, 0) for i in range(5)]) == 1)

# Link assigned and amb: if assigned[i] is True, then amb[i] ∈ {1,2,3}; else amb[i] = 0
for i in range(5):
    solver.add(Implies(assigned[i], And(amb[i] >= 1, amb[i] <= 3)))
    solver.add(Implies(Not(assigned[i]), amb[i] == 0))

# Constraint A: Exactly one of Kayne (1) or Novetzke (3) is assigned
solver.add(Xor(assigned[1], assigned[3]))

# Constraint B: If Jaramillo (0) is assigned, then Kayne (1) must be assigned
solver.add(Implies(assigned[0], assigned[1]))

# Constraint C: If Ong (4) is assigned to Venezuela (1) AND Kayne (1) is assigned to Yemen (2), then contradiction
solver.add(Not(And(amb[4] == 1, amb[1] == 2)))

# Constraint D: If Landon (2) is assigned, then amb[2] == 3 (Zambia)
solver.add(Implies(assigned[2], amb[2] == 3))

# Answer choices (pairs of candidates who are NOT assigned)
answer_choices = [
    [0, 3],  # Jaramillo and Novetzke
    [0, 4],  # Jaramillo and Ong
    [1, 2],  # Kayne and Landon
    [1, 3],  # Kayne and Novetzke
    [2, 4]   # Landon and Ong
]

answer_index_list = []

for idx, pair in enumerate(answer_choices):
    i, j = pair
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert that exactly candidates i and j are unassigned
    for k in range(5):
        if k == i or k == j:
            s_chk.add(Not(assigned[k]))
        else:
            s_chk.add(assigned[k])
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)