from z3 import *

# Witness indices: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
witnesses = 5

# Day variables: 0=Monday, 1=Tuesday, 2=Wednesday
day = [Int(f"day_{i}") for i in range(witnesses)]

# Base solver
solver = Solver()

# Domain constraints: each witness testifies on Monday, Tuesday, or Wednesday
for i in range(witnesses):
    solver.add(Or(day[i] == 0, day[i] == 1, day[i] == 2))

# Fixed constraint: Iturbe testifies on Wednesday
solver.add(day[3] == 2)

# At-least-one-Monday constraint
solver.add(Or(*[day[i] == 0 for i in range(witnesses)]))

# Exactly-two-on-Tuesday constraint
solver.add(Sum([If(day[i] == 1, 1, 0) for i in range(witnesses)]) == 2)

# Garcia-Franco-different-days constraint
solver.add(day[0] != day[1])

# Hong-not-Monday constraint
solver.add(day[2] != 0)

# Conditional assumption: Franco testifies on the same day as Hong
solver.add(day[0] == day[2])

# Answer choices (indices correspond to the order in the problem)
# A: Franco on Wednesday -> day[0] == 2
# B: Garcia on Monday -> day[1] == 0
# C: Garcia on Wednesday -> day[1] == 2
# D: Hong on Tuesday -> day[2] == 1
# E: Iturbe is the only witness on Wednesday -> exactly one witness (Iturbe) has day[w] == 2

answer_index_list = []

# Check each answer choice: must be true if its negation leads to UNSAT
for idx, cond in enumerate([
    day[0] == 2,           # A: Franco on Wednesday
    day[1] == 0,           # B: Garcia on Monday
    day[1] == 2,           # C: Garcia on Wednesday
    day[2] == 1,           # D: Hong on Tuesday
    Sum([If(day[i] == 2, 1, 0) for i in range(witnesses)]) == 1  # E: Only Iturbe on Wednesday
]):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the negation of the answer choice condition
    s_chk.add(Not(cond))
    
    # If UNSAT, then the negation is impossible -> the original condition must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)