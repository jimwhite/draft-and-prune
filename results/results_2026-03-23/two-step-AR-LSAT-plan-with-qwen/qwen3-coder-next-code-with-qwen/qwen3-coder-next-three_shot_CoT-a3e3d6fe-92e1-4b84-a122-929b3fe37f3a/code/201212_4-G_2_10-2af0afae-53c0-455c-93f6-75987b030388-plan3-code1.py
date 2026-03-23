from z3 import *

# Witness indices: 0-Franco, 1-Garcia, 2-Hong, 3-Iturbe, 4-Jackson
# Day indices: Monday=0, Tuesday=1, Wednesday=2

d = [Int(f"d_{i}") for i in range(5)]

solver = Solver()

# Domain constraints: each witness tests on Monday, Tuesday, or Wednesday
for i in range(5):
    solver.add(Or(d[i] == 0, d[i] == 1, d[i] == 2))

# Franco and Garcia do not testify on the same day
solver.add(d[0] != d[1])

# Iturbe testifies on Wednesday
solver.add(d[3] == 2)

# Exactly two witnesses testify on Tuesday
tue_count = Sum([If(d[i] == 1, 1, 0) for i in range(5)])
solver.add(tue_count == 2)

# Hong does not testify on Monday
solver.add(d[2] != 0)

# At least one witness testifies on Monday
mon_count = Sum([If(d[i] == 0, 1, 0) for i in range(5)])
solver.add(mon_count >= 1)

# Additional assumption: Franco and Hong testify on the same day
solver.add(d[0] == d[2])

# Answer choices (as conditions that must be true)
# A: Franco is scheduled to testify on Wednesday -> d[0] == 2
# B: Garcia is scheduled to testify on Monday -> d[1] == 0
# C: Garcia is scheduled to testify on Wednesday -> d[1] == 2
# D: Hong is scheduled to testify on Tuesday -> d[2] == 1
# E: Only Iturbe testifies on Wednesday -> count of witnesses with d[i]==2 is exactly 1

answer_conditions = [
    lambda: d[0] == 2,           # A
    lambda: d[1] == 0,           # B
    lambda: d[1] == 2,           # C
    lambda: d[2] == 1,           # D
    lambda: Sum([If(d[i] == 2, 1, 0) for i in range(5)]) == 1  # E
]

answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add negation of the condition
    s_chk.add(Not(cond()))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

# The problem expects exactly one correct answer
print(answer_index_list[0] if len(answer_index_list) == 1 else answer_index_list)