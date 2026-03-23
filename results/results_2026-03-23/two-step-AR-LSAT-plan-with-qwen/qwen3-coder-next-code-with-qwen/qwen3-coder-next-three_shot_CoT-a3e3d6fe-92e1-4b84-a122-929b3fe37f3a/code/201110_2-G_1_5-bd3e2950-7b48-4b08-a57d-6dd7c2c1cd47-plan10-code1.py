from z3 import *

# Employee indices: R=Robertson, S=Souza, T=Togowa, V=Vaughn, X=Xu, Y=Young
employees = ["R", "S", "T", "V", "X", "Y"]
pos = {e: Int(f"pos_{e}") for e in employees}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6
for e in employees:
    solver.add(pos[e] >= 1, pos[e] <= 6)

# Distinctness constraint
solver.add(Distinct(*[pos[e] for e in employees]))

# Base ordering constraints
solver.add(pos["Y"] > pos["T"])  # Young > Togowa
solver.add(pos["X"] > pos["S"])  # Xu > Souza
solver.add(pos["R"] > pos["Y"])  # Robertson > Young
solver.add(pos["R"] <= 4)        # Robertson in {1,2,3,4}

# Conditional constraint: Young > Souza
solver.add(pos["Y"] > pos["S"])

# Answer choices as constraints to test
answer_choices = [
    ("Togowa is assigned parking space #1.", pos["T"] == 1),
    ("Young is assigned parking space #2.", pos["Y"] == 2),
    ("Robertson is assigned parking space #3.", pos["R"] == 3),
    ("Souza is assigned parking space #3.", pos["S"] == 3),
    ("Vaughn is assigned parking space #4.", pos["V"] == 4)
]

# Check each choice
possible_choices = []
for i, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint)
    
    if s_chk.check() == sat:
        possible_choices.append(desc)

# Output only the possible choices (only those that could be true)
print(possible_choices)