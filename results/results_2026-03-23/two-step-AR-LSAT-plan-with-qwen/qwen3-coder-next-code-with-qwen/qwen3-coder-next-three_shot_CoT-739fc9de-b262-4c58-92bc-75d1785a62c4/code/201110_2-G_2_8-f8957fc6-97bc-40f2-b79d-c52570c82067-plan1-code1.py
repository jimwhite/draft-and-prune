from z3 import *

# Candidate indices: Jaramillo=0, Kayne=1, Landon=2, Novetzke=3, Ong=4
CANDIDATES = 5
COUNTRIES = ["Venezuela", "Yemen", "Zambia"]
country_indices = {c: i for i, c in enumerate(COUNTRIES)}

# assigned[i][c] = True if candidate i is assigned to country c
assigned = [[Bool(f"assigned_{i}_{c}") for c in range(3)] for i in range(CANDIDATES)]

# Base solver
solver = Solver()

# Exactly-one-assignment per candidate (each candidate assigned to at most one country)
for i in range(CANDIDATES):
    # At most one
    for c1 in range(3):
        for c2 in range(c1 + 1, 3):
            solver.add(Not(And(assigned[i][c1], assigned[i][c2])))
    # At least one (for those who get assigned, but we'll handle total count separately)
    # Actually, we'll enforce exactly 3 assignments total and let the country constraints handle coverage

# Exactly one ambassador per country
for c in range(3):
    # At least one
    at_least = Or(*[assigned[i][c] for i in range(CANDIDATES)])
    # At most one
    at_most = And(*[Implies(assigned[i][c], Not(Or([assigned[j][c] for j in range(CANDIDATES) if i != j]))) 
                    for i in range(CANDIDATES)])
    solver.add(at_least, at_most)

# Constraint A: Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships
kayne_assigned = Or(*[assigned[1][c] for c in range(3)])
novetzke_assigned = Or(*[assigned[3][c] for c in range(3)])
solver.add(Xor(kayne_assigned, novetzke_assigned))

# Constraint B: If Jaramillo is assigned, then Kayne is also assigned
jaramillo_assigned = Or(*[assigned[0][c] for c in range(3)])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Constraint C: If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
solver.add(Implies(assigned[4][0], Not(assigned[1][1])))

# Constraint D: If Landon is assigned, it must be to Zambia
landon_assigned = Or(*[assigned[2][c] for c in range(3)])
solver.add(Implies(landon_assigned, assigned[2][2]))

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
for idx, (c1, c2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that candidates c1 and c2 are NOT assigned
    for c in range(3):
        s_chk.add(Not(assigned[c1][c]))
        s_chk.add(Not(assigned[c2][c]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)