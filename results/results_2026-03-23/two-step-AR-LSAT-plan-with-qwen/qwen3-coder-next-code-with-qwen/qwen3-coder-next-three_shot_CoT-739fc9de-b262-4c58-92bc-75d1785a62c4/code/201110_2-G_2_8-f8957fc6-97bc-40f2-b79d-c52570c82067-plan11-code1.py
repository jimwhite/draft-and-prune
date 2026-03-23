from z3 import *

# Candidate indices: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
# Country indices: 0=Venezuela, 1=Yemen, 2=Zambia

# assigned[i][c] = True if candidate i is assigned to country c
assigned = [[Bool(f"assigned_{i}_{c}") for c in range(3)] for i in range(5)]

solver = Solver()

# One-per-country constraints: each country has exactly one ambassador
for c in range(3):
    solver.add(Sum([If(assigned[i][c], 1, 0) for i in range(5)]) == 1)

# One-per-candidate constraints: each candidate gets at most one assignment
for i in range(5):
    solver.add(Sum([If(assigned[i][c], 1, 0) for c in range(3)]) <= 1)

# XOR constraint: Either Kayne or Novetzke, but not both, is assigned
kayne_assigned = Or(assigned[1][0], assigned[1][1], assigned[1][2])
novetzke_assigned = Or(assigned[3][0], assigned[3][1], assigned[3][2])
solver.add(Xor(kayne_assigned, novetzke_assigned))

# Implication: If Jaramillo is assigned, then Kayne must be assigned
jaramillo_assigned = Or(assigned[0][0], assigned[0][1], assigned[0][2])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Conditional: If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
solver.add(Implies(assigned[4][0], Not(assigned[1][1])))

# Location constraint: If Landon is assigned, he must be assigned to Zambia
landon_assigned = Or(assigned[2][0], assigned[2][1], assigned[2][2])
solver.add(Implies(landon_assigned, assigned[2][2]))

# Answer choices: pairs of candidates who are NOT assigned
answer_choices = [
    (0, 3),  # Jaramillo and Novetzke
    (0, 4),  # Jaramillo and Ong
    (1, 2),  # Kayne and Landon
    (1, 3),  # Kayne and Novetzke
    (2, 4)   # Landon and Ong
]

answer_index_list = []
for idx, (a, b) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert candidates a and b are unassigned
    for c in range(3):
        s_chk.add(Not(assigned[a][c]))
        s_chk.add(Not(assigned[b][c]))
    
    # Assert the other three candidates are each assigned exactly once
    for i in range(5):
        if i != a and i != b:
            s_chk.add(Sum([If(assigned[i][c], 1, 0) for c in range(3)]) == 1)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)