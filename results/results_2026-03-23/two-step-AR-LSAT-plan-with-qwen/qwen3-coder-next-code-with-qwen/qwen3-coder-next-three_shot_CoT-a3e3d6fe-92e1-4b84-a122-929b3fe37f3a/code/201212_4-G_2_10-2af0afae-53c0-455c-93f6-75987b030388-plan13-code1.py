from z3 import *

# Witness indices: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
# Day indices: Monday=0, Tuesday=1, Wednesday=2

day = [Int(f"day_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Fixed constraint: Iturbe testifies on Wednesday (day 2)
solver.add(day[3] == 2)

# Cardinality constraints
# Exactly two witnesses testify on Tuesday (day 1)
solver.add(Sum([If(day[i] == 1, 1, 0) for i in range(5)]) == 2)

# At least one witness testifies on Monday (day 0)
solver.add(Sum([If(day[i] == 0, 1, 0) for i in range(5)]) >= 1)

# Exclusion constraints
# Franco and Garcia do not testify on same day
solver.add(day[0] != day[1])

# Hong does not testify on Monday
solver.add(day[2] != 0)

# Conditional constraint: Franco and Hong testify on same day
solver.add(day[0] == day[2])

# Answer choices (as conditions that must be true)
answer_conditions = [
    day[0] == 2,           # A: Franco on Wednesday
    day[1] == 0,           # B: Garcia on Monday
    day[1] == 2,           # C: Garcia on Wednesday
    day[2] == 1,           # D: Hong on Tuesday
    And(*[day[i] != 2 for i in range(5) if i != 3])  # E: Iturbe is the only one on Wednesday
]

# Check each answer choice to see if it must be true
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the negation of the answer choice condition
    s_chk.add(Not(cond))
    
    # If UNSAT, then the answer choice must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)