from z3 import *

# Candidate indices: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
# Country indices: 0=Venezuela, 1=Yemen, 2=Zambia

# Assignment variables: assign[i] = country assigned to candidate i (-1 if unassigned)
assign = [Int(f"assign_{i}") for i in range(5)]

# Indicator variables: assigned[i] = 1 if candidate i is assigned, 0 otherwise
assigned = [Bool(f"assigned_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Domain constraints for assign[i]
for i in range(5):
    solver.add(Or(assign[i] == -1, assign[i] == 0, assign[i] == 1, assign[i] == 2))

# Relationship between assigned and assign
for i in range(5):
    solver.add(Implies(assigned[i], assign[i] != -1))
    solver.add(Implies(Not(assigned[i]), assign[i] == -1))

# Exactly 3 candidates are assigned
solver.add(Sum([If(assigned[i], 1, 0) for i in range(5)]) == 3)

# One ambassador per country
for c in range(3):
    solver.add(Sum([If(assign[i] == c, 1, 0) for i in range(5)]) == 1)

# Constraint A: Either Kayne or Novetzke, but not both, is assigned
solver.add(assigned[1] != assigned[3])

# Constraint B: If Jaramillo is assigned, then Kayne is assigned
solver.add(Implies(assigned[0], assigned[1]))

# Constraint C: If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
solver.add(Or(assign[4] != 0, assign[1] != 1))

# Constraint D: If Landon is assigned, then to Zambia
solver.add(Implies(assigned[2], assign[2] == 2))

# Answer choices (pairs of unassigned candidates)
answer_choices = [
    [0, 3],  # Jaramillo and Novetzke
    [0, 4],  # Jaramillo and Ong
    [1, 2],  # Kayne and Landon
    [1, 3],  # Kayne and Novetzke
    [2, 4]   # Landon and Ong
]

# Check each answer choice
answer_index_list = []
for idx, pair in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the two candidates in the pair are unassigned
    for i in pair:
        s_chk.add(Not(assigned[i]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)