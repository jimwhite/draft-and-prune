from z3 import *

# Employee indices: R=Robertson, S=Souza, T=Togowa, V=Vaughn, X=Xu, Y=Young
employees = ["R", "S", "T", "V", "X", "Y"]

# Position variables: pos[e] = assigned parking space (1-6)
pos = {e: Int(f"pos_{e}") for e in employees}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6
for e in employees:
    solver.add(pos[e] >= 1, pos[e] <= 6)

# Distinctness constraint: all positions must be different
solver.add(Distinct(*[pos[e] for e in employees]))

# Given ordering constraints from rules
solver.add(pos["Y"] > pos["T"])  # Young > Togowa
solver.add(pos["X"] > pos["S"])  # Xu > Souza
solver.add(pos["R"] > pos["Y"])  # Robertson > Young
solver.add(pos["R"] <= 4)        # Robertson in {1,2,3,4}

# Conditional assumption: Young > Souza
solver.add(pos["Y"] > pos["S"])

# Answer choices (indices correspond to the order in the list)
answer_choices = [
    ("Togowa is assigned parking space #1.", pos["T"] == 1),
    ("Young is assigned parking space #2.", pos["Y"] == 2),
    ("Robertson is assigned parking space #3.", pos["R"] == 3),
    ("Souza is assigned parking space #3.", pos["S"] == 3),
    ("Vaughn is assigned parking space #4.", pos["V"] == 4)
]

# Check each answer choice
answer_index_list = []
for idx, (_, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    # Add base constraints and conditional
    s_chk.add(solver.assertions())
    # Add the specific choice constraint
    s_chk.add(constraint)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)