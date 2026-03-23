from z3 import *

# Candidate indices: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
# Country indices: 0=Venezuela, 1=Yemen, 2=Zambia

# Assignment variables: assign[i][j] = True if candidate i is assigned to country j
assign = [[Bool(f"assign_{i}_{j}") for j in range(3)] for i in range(5)]

solver = Solver()

# Constraint 3: Each country gets exactly one ambassador
for j in range(3):
    solver.add(Sum([If(assign[i][j], 1, 0) for i in range(5)]) == 1)

# Constraint 3: Each candidate gets at most one country
for i in range(5):
    solver.add(Sum([If(assign[i][j], 1, 0) for j in range(3)]) <= 1)

# Constraint A: Exactly one of Kayne (1) or Novetzke (3) is assigned
kayne_sum = Sum([If(assign[1][j], 1, 0) for j in range(3)])
novetzke_sum = Sum([If(assign[3][j], 1, 0) for j in range(3)])
solver.add(kayne_sum + novetzke_sum == 1)

# Constraint B: If Jaramillo is assigned, then Kayne must be assigned
jaramillo_sum = Sum([If(assign[0][j], 1, 0) for j in range(3)])
solver.add(jaramillo_sum <= kayne_sum)

# Constraint C: If Ong is assigned to Venezuela, then Kayne must not be assigned to Yemen
solver.add(Or(Not(assign[4][0]), Not(assign[1][1])))

# Constraint D: If Landon is assigned, it must be to Zambia
solver.add(Not(assign[2][0]))
solver.add(Not(assign[2][1]))

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
    
    # Add constraints that candidates c1 and c2 are not assigned
    for j in range(3):
        s_chk.add(Not(assign[c1][j]))
        s_chk.add(Not(assign[c2][j]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)