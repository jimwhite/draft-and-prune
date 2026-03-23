from z3 import *

# Candidate indices: Jaramillo=0, Kayne=1, Landon=2, Novetzke=3, Ong=4
# Country indices: Venezuela=0, Yemen=1, Zambia=2

assign = [[Bool(f"assign_{i}_{c}") for c in range(3)] for i in range(5)]

solver = Solver()

# Each candidate assigned to at most one country
for i in range(5):
    # At most one: sum <= 1, but since we'll enforce exactly three ambassadors total,
    # and each country gets exactly one, this will be handled by the country constraints.
    # We'll add: not (assign[i][0] and assign[i][1]) etc.
    solver.add(Not(And(assign[i][0], assign[i][1])))
    solver.add(Not(And(assign[i][0], assign[i][2])))
    solver.add(Not(And(assign[i][1], assign[i][2])))

# Each country gets exactly one ambassador
for c in range(3):
    # Exactly one: sum == 1
    country_assignments = [assign[i][c] for i in range(5)]
    solver.add(AtMost(*country_assignments, 1))
    solver.add(Or(*country_assignments))

# Kayne or Novetzke but not both assigned (XOR on being assigned to any country)
kayne_assigned = Or(assign[1][0], assign[1][1], assign[1][2])
novetzke_assigned = Or(assign[3][0], assign[3][1], assign[3][2])
solver.add(Xor(kayne_assigned, novetzke_assigned))

# If Jaramillo is assigned, then Kayne must be assigned
jaramillo_assigned = Or(assign[0][0], assign[0][1], assign[0][2])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
solver.add(Implies(assign[4][0], Not(assign[1][1])))

# If Landon is assigned, it must be to Zambia
# So Landon cannot be assigned to Venezuela or Yemen
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
for idx, (i1, i2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert that candidates i1 and i2 are not assigned to any country
    for c in range(3):
        s_chk.add(Not(assign[i1][c]))
        s_chk.add(Not(assign[i2][c]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)