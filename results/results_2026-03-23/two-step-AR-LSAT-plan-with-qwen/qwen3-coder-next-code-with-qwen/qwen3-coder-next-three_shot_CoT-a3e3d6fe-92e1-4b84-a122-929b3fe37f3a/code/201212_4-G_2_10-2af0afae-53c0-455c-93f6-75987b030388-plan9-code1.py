from z3 import *

# Witness indices: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
# Day indices: Monday=0, Tuesday=1, Wednesday=2

day = [Int(f"day_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Domain constraints: each witness testifies on Monday, Tuesday, or Wednesday
for i in range(5):
    solver.add(Or(day[i] == 0, day[i] == 1, day[i] == 2))

# Fixed constraints
solver.add(day[3] == 2)  # Iturbe testifies on Wednesday

# Cardinality constraints
solver.add(Sum([If(day[i] == 1, 1, 0) for i in range(5)]) == 2)  # Exactly two on Tuesday
solver.add(Sum([If(day[i] == 0, 1, 0) for i in range(5)]) >= 1)   # At least one on Monday

# Mutual exclusion constraints
solver.add(day[0] != day[1])  # Franco and Garcia not on same day
solver.add(day[2] != 0)       # Hong does not testify on Monday

# Conditional assumption: Franco and Hong testify on same day
solver.add(day[0] == day[2])

# Answer choices (as conditions)
choices = [
    day[0] == 2,                    # A: Franco on Wednesday
    day[1] == 0,                    # B: Garcia on Monday
    day[1] == 2,                    # C: Garcia on Wednesday
    day[2] == 1,                    # D: Hong on Tuesday
    Sum([If(day[i] == 2, 1, 0) for i in range(5)]) == 1  # E: Iturbe is the only one on Wednesday
]

# Check each choice using proof by contradiction (negation)
answer_index_list = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add negation of the choice
    s_chk.add(Not(choice))
    
    # If UNSAT, then the choice must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)