from z3 import *

# Candidate indices: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
# Country indices: 0=Venezuela, 1=Yemen, 2=Zambia

# assigned[i][c] = True if candidate i is assigned to country c
assigned = [[Bool(f"assigned_{i}_{c}") for c in range(3)] for i in range(5)]

# Base solver
solver = Solver()

# Assignment constraints: each country gets exactly one ambassador
for c in range(3):
    solver.add(Sum([If(assigned[i][c], 1, 0) for i in range(5)]) == 1)

# Each candidate is assigned to at most one country
for i in range(5):
    solver.add(Sum([If(assigned[i][c], 1, 0) for c in range(3)]) <= 1)

# Constraint: exactly one of Kayne (1) or Novetzke (3) is assigned to some ambassadorship
kayne_total = Sum([If(assigned[1][c], 1, 0) for c in range(3)])
novetzke_total = Sum([If(assigned[3][c], 1, 0) for c in range(3)])
solver.add(kayne_total + novetzke_total == 1)

# Conditional: If Jaramillo (0) is assigned, then Kayne (1) must also be assigned
jaramillo_assigned = Or(assigned[0][0], assigned[0][1], assigned[0][2])
kayne_assigned = Or(assigned[1][0], assigned[1][1], assigned[1][2])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Conditional: If Ong (4) is assigned to Venezuela (0), then Kayne (1) cannot be assigned to Yemen (1)
solver.add(Implies(assigned[4][0], Not(assigned[1][1])))

# Conditional: If Landon (2) is assigned, it must be to Zambia (2)
solver.add(Not(assigned[2][0]))  # Landon not to Venezuela
solver.add(Not(assigned[2][1]))  # Landon not to Yemen

# Answer choices pairs (indices of candidates who are NOT assigned)
answer_choices = [
    (0, 3),  # Jaramillo and Novetzke
    (0, 4),  # Jaramillo and Ong
    (1, 2),  # Kayne and Landon
    (1, 3),  # Kayne and Novetzke
    (2, 4)   # Landon and Ong
]

# Check each answer choice
answer_index_list = []
for idx, (c1, c2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert that candidates c1 and c2 are NOT assigned to any country
    for c in range(3):
        s_chk.add(Not(assigned[c1][c]))
        s_chk.add(Not(assigned[c2][c]))
    
    # Check satisfiability
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)