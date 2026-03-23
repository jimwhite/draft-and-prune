from z3 import *

# Candidate indices: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
# Country indices: 0=Venezuela, 1=Yemen, 2=Zambia

# assigned[i][c] = True if candidate i is assigned to country c
assigned = [[Bool(f"assigned_{i}_{c}") for c in range(3)] for i in range(5)]

# Base solver
solver = Solver()

# One-assignment-per-candidate: each candidate assigned to at most one country
for i in range(5):
    # At most one country per candidate
    for c1 in range(3):
        for c2 in range(c1 + 1, 3):
            solver.add(Not(assigned[i][c1], assigned[i][c2]))

# One-candidate-per-country: each country has exactly one ambassador
for c in range(3):
    # At least one candidate per country
    solver.add(Or([assigned[i][c] for i in range(5)]))
    # At most one candidate per country
    for i1 in range(5):
        for i2 in range(i1 + 1, 5):
            solver.add(Not(assigned[i1][c], assigned[i2][c]))

# Constraint 1: Exactly one of Kayne (1) or Novetzke (3) is assigned
kayne_assigned = Or([assigned[1][c] for c in range(3)])
novetzke_assigned = Or([assigned[3][c] for c in range(3)])
solver.add(Xor(kayne_assigned, novetzke_assigned))

# Constraint 2: If Jaramillo is assigned, then Kayne must be assigned
jaramillo_assigned = Or([assigned[0][c] for c in range(3)])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Constraint 3: If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
solver.add(Implies(assigned[4][0], Not(assigned[1][1])))

# Constraint 4: If Landon is assigned, it must be to Zambia
# So Landon cannot be assigned to Venezuela or Yemen
solver.add(Not(assigned[2][0]))
solver.add(Not(assigned[2][1]))

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
for idx, (i, j) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that candidates i and j are NOT assigned to any country
    for c in range(3):
        s_chk.add(Not(assigned[i][c]))
        s_chk.add(Not(assigned[j][c]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)