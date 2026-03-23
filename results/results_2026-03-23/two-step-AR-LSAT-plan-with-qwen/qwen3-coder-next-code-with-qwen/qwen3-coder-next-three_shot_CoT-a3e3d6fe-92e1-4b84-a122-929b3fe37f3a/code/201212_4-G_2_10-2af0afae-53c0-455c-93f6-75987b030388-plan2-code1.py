from z3 import *

# Witness indices: 0-Franco, 1-Garcia, 2-Hong, 3-Iturbe, 4-Jackson
witnesses = ["Franco", "Garcia", "Hong", "Iturbe", "Jackson"]
day_vars = [Int(f"day_{w}") for w in witnesses]

# Base solver
solver = Solver()

# Domain constraints: each witness tests on day 1 (Mon), 2 (Tue), or 3 (Wed)
for d in day_vars:
    solver.add(And(d >= 1, d <= 3))

# Iturbe testifies on Wednesday (day 3)
solver.add(day_vars[3] == 3)

# Exactly two witnesses testify on Tuesday (day 2)
solver.add(Sum([If(d == 2, 1, 0) for d in day_vars]) == 2)

# Franco and Garcia do not testify on the same day
solver.add(day_vars[0] != day_vars[1])

# Hong does not testify on Monday (day 1)
solver.add(day_vars[2] != 1)

# At least one witness testifies on Monday (day 1)
solver.add(Sum([If(d == 1, 1, 0) for d in day_vars]) >= 1)

# Given condition: Franco and Hong testify on the same day
solver.add(day_vars[0] == day_vars[2])

# Answer choices propositions (as Z3 expressions)
# A: Franco = 3
prop_A = (day_vars[0] == 3)
# B: Garcia = 1
prop_B = (day_vars[1] == 1)
# C: Garcia = 3
prop_C = (day_vars[1] == 3)
# D: Hong = 2
prop_D = (day_vars[2] == 2)
# E: Only Iturbe on Wednesday → day count for Wed = 1
count_wed = Sum([If(d == 3, 1, 0) for d in day_vars])
prop_E = (count_wed == 1)

answer_props = [prop_A, prop_B, prop_C, prop_D, prop_E]

# Check which answer must be true (i.e., negation leads to UNSAT)
answer_index_list = []
for idx, prop in enumerate(answer_props):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    # Add negation of the choice
    s_chk.add(Not(prop))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)