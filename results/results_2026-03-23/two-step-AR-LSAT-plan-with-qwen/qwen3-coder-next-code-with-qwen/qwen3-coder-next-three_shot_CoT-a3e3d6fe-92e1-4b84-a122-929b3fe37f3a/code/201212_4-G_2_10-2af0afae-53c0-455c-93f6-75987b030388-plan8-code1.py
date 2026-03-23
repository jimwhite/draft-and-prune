from z3 import *

# Witness indices: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
# Day indices: Monday=0, Tuesday=1, Wednesday=2

day = [Int(f"day_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Domain constraints: each witness testifies on Monday, Tuesday, or Wednesday
for i in range(5):
    solver.add(Or(day[i] == 0, day[i] == 1, day[i] == 2))

# Fixed constraint: Iturbe testifies on Wednesday
solver.add(day[3] == 2)

# Tuesday count constraint: exactly two witnesses testify on Tuesday
solver.add(Sum([If(day[i] == 1, 1, 0) for i in range(5)]) == 2)

# Monday at-least-one constraint: at least one witness testifies on Monday
solver.add(Sum([If(day[i] == 0, 1, 0) for i in range(5)]) >= 1)

# Hong not Monday constraint
solver.add(day[2] != 0)

# Franco-Garcia different day constraint
solver.add(day[0] != day[1])

# Assumed condition: Franco testifies on same day as Hong
solver.add(day[0] == day[2])

# Answer choices (to check necessity)
answer_choices = [
    day[0] == 2,          # Choice 0: Franco on Wednesday
    day[1] == 0,          # Choice 1: Garcia on Monday
    day[1] == 2,          # Choice 2: Garcia on Wednesday
    day[2] == 1,          # Choice 3: Hong on Tuesday
    Sum([If(day[i] == 2, 1, 0) for i in range(5)]) == 1  # Choice 4: Iturbe only on Wednesday
]

# Check each answer choice for necessity
answer_index_list = []
for i in range(5):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the negation of choice i
    s_chk.add(Not(answer_choices[i]))
    
    # If UNSAT, then choice i must be true
    if s_chk.check() == unsat:
        answer_index_list.append(i)

print(answer_index_list)