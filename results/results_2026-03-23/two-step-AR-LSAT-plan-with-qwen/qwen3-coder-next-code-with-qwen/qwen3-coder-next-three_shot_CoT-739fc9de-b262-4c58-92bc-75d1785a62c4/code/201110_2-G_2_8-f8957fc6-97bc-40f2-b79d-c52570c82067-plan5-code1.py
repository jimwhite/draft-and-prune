from z3 import *

# Candidate indices: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
# Country indices: 0=Venezuela, 1=Yemen, 2=Zambia

# x[i][c] = True if candidate i is assigned to country c
x = [[Bool(f"x_{i}_{c}") for c in range(3)] for i in range(5)]

# Base solver
solver = Solver()

# Exactly one ambassador per country
for c in range(3):
    solver.add(Sum([If(x[i][c], 1, 0) for i in range(5)]) == 1)

# Each candidate assigned to at most one country
for i in range(5):
    # At most one country per candidate
    for c1 in range(3):
        for c2 in range(c1+1, 3):
            solver.add(Not(x[i][c1], x[i][c2]))

# Constraint 1: Exactly one of Kayne or Novetzke is assigned (XOR)
kayne_assigned = Or(x[1][0], x[1][1], x[1][2])
novetzke_assigned = Or(x[3][0], x[3][1], x[3][2])
solver.add(Xor(kayne_assigned, novetzke_assigned))

# Constraint 2: If Jaramillo is assigned, then Kayne is also assigned
jaramillo_assigned = Or(x[0][0], x[0][1], x[0][2])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Constraint 3: If Ong is assigned to Venezuela, then Kayne is NOT assigned to Yemen
solver.add(Implies(x[4][0], Not(x[1][1])))

# Constraint 4: If Landon is assigned, it must be to Zambia
# So Landon cannot be assigned to Venezuela or Yemen
solver.add(Not(x[2][0]))
solver.add(Not(x[2][1]))

# Answer choices: pairs of candidates who are NOT assigned
answer_choices = [
    (0, 3),  # Jaramillo and Novetzke
    (0, 4),  # Jaramillo and Ong
    (1, 2),  # Kayne and Landon
    (1, 3),  # Kayne and Novetzke
    (2, 4)   # Landon and Ong
]

# Check each answer choice
answer_index_list = []
for idx, (i1, i2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert that candidates i1 and i2 are NOT assigned (all their country assignments False)
    for c in range(3):
        s_chk.add(Not(x[i1][c]))
        s_chk.add(Not(x[i2][c]))
    
    # The other three candidates must each be assigned to exactly one country
    for i in range(5):
        if i != i1 and i != i2:
            s_chk.add(Sum([If(x[i][c], 1, 0) for c in range(3)]) == 1)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)