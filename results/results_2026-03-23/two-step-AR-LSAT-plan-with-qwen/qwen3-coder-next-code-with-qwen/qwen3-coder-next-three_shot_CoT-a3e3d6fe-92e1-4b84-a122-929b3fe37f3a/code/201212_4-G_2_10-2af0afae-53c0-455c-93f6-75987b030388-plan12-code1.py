from z3 import *

# Witness indices: 0-Franco, 1-Garcia, 2-Hong, 3-Iturbe, 4-Jackson
(F, G, H, I, J) = range(5)

# Day variables: 0-Monday, 1-Tuesday, 2-Wednesday
d = [Int(f"d_{w}") for w in range(5)]

# Base solver
solver = Solver()

# Domain constraints: each witness tests on Monday, Tuesday, or Wednesday
for w in range(5):
    solver.add(d[w] >= 0, d[w] <= 2)

# Fixed constraint: Iturbe testifies on Wednesday
solver.add(d[I] == 2)

# Tuesday has exactly two witnesses
tue_count = Sum([If(d[w] == 1, 1, 0) for w in range(5)])
solver.add(tue_count == 2)

# Monday has at least one witness
mon_count = Sum([If(d[w] == 0, 1, 0) for w in range(5)])
solver.add(mon_count >= 1)

# Franco and Garcia do not testify on the same day
solver.add(d[F] != d[G])

# Hong does not testify on Monday
solver.add(d[H] != 0)

# Assumed condition: Franco and Hong testify on the same day
solver.add(d[F] == d[H])

# Answer choices (as conditions to check necessity)
answer_conditions = [
    # A: Franco is scheduled to testify on Wednesday
    d[F] == 2,
    # B: Garcia is scheduled to testify on Monday
    d[G] == 0,
    # C: Garcia is scheduled to testify on Wednesday
    d[G] == 2,
    # D: Hong is scheduled to testify on Tuesday
    d[H] == 1,
    # E: Iturbe is the only witness scheduled to testify on Wednesday
    And(d[I] == 2, 
        d[F] != 2, d[G] != 2, d[H] != 2, d[J] != 2)
]

# Check which answer choices must be true (i.e., their negation is UNSAT)
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add negation of the answer choice condition
    s_chk.add(Not(cond))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

# Output the index of the forced statement
print(answer_index_list[0] if answer_index_list else -1)