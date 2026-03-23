from z3 import *

# Witness indices: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
witnesses = ["Franco", "Garcia", "Hong", "Iturbe", "Jackson"]
day = [Int(f"day_{w}") for w in witnesses]

# Base solver
solver = Solver()

# Domain constraints: each day is 1 (Monday), 2 (Tuesday), or 3 (Wednesday)
for d in day:
    solver.add(And(d >= 1, d <= 3))

# Global constraints
# At least one witness on Monday
solver.add(Or(*[d == 1 for d in day]))

# Exactly two witnesses on Tuesday
solver.add(Sum([If(d == 2, 1, 0) for d in day]) == 2)

# Iturbe testifies on Wednesday
solver.add(day[3] == 3)

# Franco does not testify on the same day as Garcia
solver.add(day[0] != day[1])

# Hong does not testify on Monday
solver.add(day[2] != 1)

# Conditional assumption: Franco and Hong testify on the same day
solver.add(day[0] == day[2])

# Answer choices (as logical statements to check if they must be true)
# A. Franco is scheduled to testify on Wednesday: day[0] == 3
# B. Garcia is scheduled to testify on Monday: day[1] == 1
# C. Garcia is scheduled to testify on Wednesday: day[1] == 3
# D. Hong is scheduled to testify on Tuesday: day[2] == 2
# E. Iturbe is the only witness scheduled to testify on Wednesday: 
#    For all witnesses w, if day[w] == 3 then w == Iturbe (index 3)

answer_choices = [
    "Franco is scheduled to testify on Wednesday.",
    "Garcia is scheduled to testify on Monday.",
    "Garcia is scheduled to testify on Wednesday.",
    "Hong is scheduled to testify on Tuesday.",
    "Iturbe is the only witness scheduled to testify on Wednesday."
]

answer_index_list = []

# Check each choice by negating and testing unsatisfiability
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    if idx == 0:  # A: Franco on Wednesday
        s_chk.add(day[0] != 3)
    elif idx == 1:  # B: Garcia on Monday
        s_chk.add(day[1] != 1)
    elif idx == 2:  # C: Garcia on Wednesday
        s_chk.add(day[1] != 3)
    elif idx == 3:  # D: Hong on Tuesday
        s_chk.add(day[2] != 2)
    elif idx == 4:  # E: Iturbe is the only one on Wednesday
        # Negation: at least one other witness besides Iturbe is on Wednesday
        s_chk.add(Or(*[And(d == 3, i != 3) for i, d in enumerate(day)]))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)