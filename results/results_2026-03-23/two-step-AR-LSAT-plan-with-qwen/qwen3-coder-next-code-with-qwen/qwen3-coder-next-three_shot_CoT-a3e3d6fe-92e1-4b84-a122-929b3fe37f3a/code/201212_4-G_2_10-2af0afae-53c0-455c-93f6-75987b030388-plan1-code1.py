from z3 import *

# Witness indices: 0-Franco, 1-Garcia, 2-Hong, 3-Iturbe, 4-Jackson
# Day indices: 0-Monday, 1-Tuesday, 2-Wednesday

f = Int('f')  # Franco's day
g = Int('g')  # Garcia's day
h = Int('h')  # Hong's day
i = Int('i')  # Iturbe's day
j = Int('j')  # Jackson's day

solver = Solver()

# Fixed constraint: Iturbe testifies on Wednesday
solver.add(i == 2)

# No-same-day constraint: Franco and Garcia do not testify on same day
solver.add(f != g)

# Hong constraint: Hong does not testify on Monday
solver.add(h != 0)

# Tuesday constraint: exactly two witnesses testify on Tuesday
tuesday_count = If(f == 1, 1, 0) + If(g == 1, 1, 0) + If(h == 1, 1, 0) + If(i == 1, 1, 0) + If(j == 1, 1, 0)
solver.add(tuesday_count == 2)

# Monday constraint: at least one witness testifies on Monday
monday_count = If(f == 0, 1, 0) + If(g == 0, 1, 0) + If(h == 0, 1, 0) + If(i == 0, 1, 0) + If(j == 0, 1, 0)
solver.add(monday_count >= 1)

# Hypothesis constraint: Franco and Hong testify on same day
solver.add(f == h)

# Answer choices (indices): 
# 0: Franco = Wednesday (f == 2)
# 1: Garcia = Monday (g == 0)
# 2: Garcia = Wednesday (g == 2)
# 3: Hong = Tuesday (h == 1)
# 4: Iturbe is the only witness on Wednesday (i == 2 and exactly one person has day == 2)

must_be_true_indices = []

# Check each answer choice
for idx, cond in enumerate([
    f == 2,           # A: Franco = Wednesday
    g == 0,           # B: Garcia = Monday
    g == 2,           # C: Garcia = Wednesday
    h == 1,           # D: Hong = Tuesday
    And(i == 2, 
        If(f == 2, 1, 0) + If(g == 2, 1, 0) + If(h == 2, 1, 0) + If(i == 2, 1, 0) + If(j == 2, 1, 0) == 1)  # E: Only Iturbe on Wednesday
]):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Negate the condition
    s_chk.add(Not(cond))
    
    if s_chk.check() == unsat:
        must_be_true_indices.append(idx)

print(must_be_true_indices)