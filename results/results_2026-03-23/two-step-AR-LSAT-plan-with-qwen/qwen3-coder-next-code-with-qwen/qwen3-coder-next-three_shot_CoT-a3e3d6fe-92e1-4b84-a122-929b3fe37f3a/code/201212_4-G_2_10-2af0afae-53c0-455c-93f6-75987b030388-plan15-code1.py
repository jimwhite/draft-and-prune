from z3 import *

# Witness indices: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
witnesses = ["Franco", "Garcia", "Hong", "Iturbe", "Jackson"]
day = [Int(f"day_{w}") for w in witnesses]

# Base solver
solver = Solver()

# Domain constraints: each day is 1 (Monday), 2 (Tuesday), or 3 (Wednesday)
for d in day:
    solver.add(Or(d == 1, d == 2, d == 3))

# Fixed constraint: Iturbe testifies on Wednesday
solver.add(day[3] == 3)

# Exactly two witnesses testify on Tuesday
solver.add(Sum([If(d == 2, 1, 0) for d in day]) == 2)

# Hong does not testify on Monday
solver.add(day[2] != 1)

# At least one witness testifies on Monday
solver.add(Sum([If(d == 1, 1, 0) for d in day]) >= 1)

# Franco and Garcia do not testify on the same day
solver.add(day[0] != day[1])

# Problem-specific assumption: Franco and Hong testify on the same day
solver.add(day[0] == day[2])

# Answer choices (as constraints that must be true)
answer_constraints = [
    day[0] == 3,                    # Franco is scheduled to testify on Wednesday
    day[1] == 1,                    # Garcia is scheduled to testify on Monday
    day[1] == 3,                    # Garcia is scheduled to testify on Wednesday
    day[2] == 2,                    # Hong is scheduled to testify on Tuesday
    And(day[3] == 3,                # Iturbe is the only witness scheduled to testify on Wednesday
        Sum([If(d == 3, 1, 0) for d in day]) == 1)
]

# Check each answer choice using proof by contradiction
answer_index_list = []
for idx, constraint in enumerate(answer_constraints):
    s_chk = Solver()
    # Add base constraints and the Franco-Hong same-day assumption
    s_chk.add(solver.assertions())
    
    # Assert the negation of the answer choice
    s_chk.add(Not(constraint))
    
    # If UNSAT, then the answer choice must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)