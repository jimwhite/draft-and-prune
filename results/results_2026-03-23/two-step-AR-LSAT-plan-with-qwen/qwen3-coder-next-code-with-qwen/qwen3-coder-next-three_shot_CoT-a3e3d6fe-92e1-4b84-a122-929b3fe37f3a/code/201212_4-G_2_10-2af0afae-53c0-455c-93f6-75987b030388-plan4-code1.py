from z3 import *

# Witness indices: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
# Day indices: Monday=0, Tuesday=1, Wednesday=2

day = [Int(f"day_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Fixed constraint: Iturbe testifies on Wednesday (day 2)
solver.add(day[3] == 2)

# Distinct-day constraint: Franco and Garcia do not testify on the same day
solver.add(day[0] != day[1])

# Count constraint for Tuesday: Exactly two witnesses testify on Tuesday (day 1)
solver.add(Sum([If(day[i] == 1, 1, 0) for i in range(5)]) == 2)

# Hong constraint: Hong does not testify on Monday (day 0)
solver.add(day[2] != 0)

# Monday coverage constraint: At least one witness testifies on Monday (day 0)
solver.add(Or([day[i] == 0 for i in range(5)]))

# Hypothesis constraint: Franco and Hong testify on the same day
solver.add(day[0] == day[2])

# Answer choices (as conditions that must be true)
# A: Franco is scheduled to testify on Wednesday → day[0] == 2
# B: Garcia is scheduled to testify on Monday → day[1] == 0
# C: Garcia is scheduled to testify on Wednesday → day[1] == 2
# D: Hong is scheduled to testify on Tuesday → day[2] == 1
# E: Iturbe is the only witness scheduled to testify on Wednesday → count of day[i] == 2 equals 1

answer_conditions = [
    day[0] == 2,           # A
    day[1] == 0,           # B
    day[1] == 2,           # C
    day[2] == 1,           # D
    Sum([If(day[i] == 2, 1, 0) for i in range(5)]) == 1  # E
]

# Check which answer choices must be true (i.e., their negation leads to UNSAT)
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the negation of the answer choice
    s_chk.add(Not(cond))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)