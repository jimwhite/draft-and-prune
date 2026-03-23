from z3 import *

# Candidate indices: 0-Jaramillo, 1-Kayne, 2-Landon, 3-Novetzke, 4-Ong
# Country indices: 0-Venezuela, 1-Yemen, 2-Zambia

# assign[i][j] = True if candidate j is assigned to country i
assign = [[Bool(f"assign_{i}_{j}") for j in range(5)] for i in range(3)]

solver = Solver()

# One-per-country constraints: each country gets exactly one ambassador
for i in range(3):
    solver.add(Sum([If(assign[i][j], 1, 0) for j in range(5)]) == 1)

# One-per-candidate constraints: each candidate gets at most one assignment
for j in range(5):
    solver.add(Sum([If(assign[i][j], 1, 0) for i in range(3)]) <= 1)

# Constraint A: Exactly one of Kayne (1) or Novetzke (3) is assigned
kayne_assigned = Or(assign[0][1], assign[1][1], assign[2][1])
novetzke_assigned = Or(assign[0][3], assign[1][3], assign[2][3])
solver.add(Xor(kayne_assigned, novetzke_assigned))

# Constraint B: If Jaramillo is assigned, then Kayne must also be assigned
jaramillo_assigned = Or(assign[0][0], assign[1][0], assign[2][0])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Constraint C: If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
solver.add(Implies(assign[0][4], Not(assign[1][1])))

# Constraint D: If Landon is assigned, it must be to Zambia
# So Landon cannot be assigned to Venezuela or Yemen
solver.add(Not(assign[0][2]))
solver.add(Not(assign[1][2]))

# Answer choices: pairs of candidates who are NOT assigned
answer_choices = [
    (0, 3),  # Jaramillo and Novetzke
    (0, 4),  # Jaramillo and Ong
    (1, 2),  # Kayne and Landon
    (1, 3),  # Kayne and Novetzke
    (2, 4)   # Landon and Ong
]

answer_index_list = []
for idx, (c1, c2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert that candidates c1 and c2 are NOT assigned to any country
    for i in range(3):
        s_chk.add(Not(assign[i][c1]))
        s_chk.add(Not(assign[i][c2]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)