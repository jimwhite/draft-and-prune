from z3 import *

# Candidate indices: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
CANDIDATES = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]
C = len(CANDIDATES)

# Country indices: 0=Venezuela, 1=Yemen, 2=Zambia
COUNTRIES = ["Venezuela", "Yemen", "Zambia"]
R = len(COUNTRIES)

# Assignment variables: assign[i][j] = True if candidate i assigned to country j
assign = [[Bool(f"assign_{i}_{j}") for j in range(R)] for i in range(C)]

# Base solver
solver = Solver()

# One-assignment-per-candidate constraints: at most one country per candidate
for i in range(C):
    # At most one (already handled by distinctness of assignments, but we add explicit constraint)
    for j1 in range(R):
        for j2 in range(j1 + 1, R):
            solver.add(Not(assign[i][j1], assign[i][j2]))

# One-candidate-per-country constraints: exactly one candidate per country
for j in range(R):
    # At least one
    solver.add(Or([assign[i][j] for i in range(C)]))
    # At most one
    for i1 in range(C):
        for i2 in range(i1 + 1, C):
            solver.add(Not(assign[i1][j], assign[i2][j]))

# Kayne/Novetzke XOR constraint: exactly one of them is assigned to any country
kayne_assigned = Or([assign[1][j] for j in range(R)])
novetzke_assigned = Or([assign[3][j] for j in range(R)])
solver.add(Xor(kayne_assigned, novetzke_assigned))

# Jaramillo → Kayne constraint: if Jaramillo is assigned anywhere, then Kayne must be assigned somewhere
jaramillo_assigned = Or([assign[0][j] for j in range(R)])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Ong → Kayne (Venezuela-Yemen) constraint: If Ong is assigned to Venezuela, then Kayne is NOT assigned to Yemen
# i.e., assign[4][0] ⇒ ¬assign[1][1]
solver.add(Implies(assign[4][0], Not(assign[1][1])))

# Landon → Zambia constraint: Landon can only be assigned to Zambia
# So assign[2][0] and assign[2][1] must be False
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

# Check each answer choice
answer_index_list = []
for idx, (c1, c2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Enforce that candidates c1 and c2 are NOT assigned to any country
    for j in range(R):
        s_chk.add(Not(assign[c1][j]))
        s_chk.add(Not(assign[c2][j]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)