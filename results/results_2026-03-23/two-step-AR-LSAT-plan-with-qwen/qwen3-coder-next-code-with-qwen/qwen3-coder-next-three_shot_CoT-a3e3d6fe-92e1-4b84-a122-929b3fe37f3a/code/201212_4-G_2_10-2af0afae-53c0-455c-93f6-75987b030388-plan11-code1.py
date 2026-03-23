from z3 import *

# Witness indices: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
# Day indices: Monday=0, Tuesday=1, Wednesday=2

d = [Int(f"d_{i}") for i in range(5)]

solver = Solver()

# Fixed constraint: Iturbe testifies on Wednesday
solver.add(d[3] == 2)

# Tuesday has exactly two witnesses
tue_count = Sum([If(d[i] == 1, 1, 0) for i in range(5)])
solver.add(tue_count == 2)

# Monday has at least one witness
mon_count = Sum([If(d[i] == 0, 1, 0) for i in range(5)])
solver.add(mon_count >= 1)

# Franco and Garcia do not testify on same day
solver.add(d[0] != d[1])

# Hong does not testify on Monday
solver.add(d[2] != 0)

# Additional constraint from question: Franco and Hong testify on same day
solver.add(d[0] == d[2])

# Answer choices (as logical conditions):
# 0: Franco is scheduled to testify on Wednesday. -> d[0] == 2
# 1: Garcia is scheduled to testify on Monday. -> d[1] == 0
# 2: Garcia is scheduled to testify on Wednesday. -> d[1] == 2
# 3: Hong is scheduled to testify on Tuesday. -> d[2] == 1
# 4: Iturbe is the only witness scheduled to testify on Wednesday. -> 
#    (d[3] == 2) and (for all other witnesses i != 3, d[i] != 2)

# Check each answer choice
answer_index_list = []

# For choice 0: Franco on Wednesday (d[0] == 2)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(d[0] != 2)  # Negation
if s_chk.check() == unsat:
    answer_index_list.append(0)

# For choice 1: Garcia on Monday (d[1] == 0)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(d[1] != 0)  # Negation
if s_chk.check() == unsat:
    answer_index_list.append(1)

# For choice 2: Garcia on Wednesday (d[1] == 2)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(d[1] != 2)  # Negation
if s_chk.check() == unsat:
    answer_index_list.append(2)

# For choice 3: Hong on Tuesday (d[2] == 1)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(d[2] != 1)  # Negation
if s_chk.check() == unsat:
    answer_index_list.append(3)

# For choice 4: Iturbe is the only witness on Wednesday
# This means: d[3] == 2 AND for all i != 3, d[i] != 2
# Negation: either d[3] != 2 OR at least one other witness is on Wednesday
s_chk = Solver()
s_chk.add(solver.assertions())
# Negation: d[3] != 2 OR (d[0]==2 OR d[1]==2 OR d[2]==2 OR d[4]==2)
s_chk.add(Or(d[3] != 2, Or(d[0] == 2, d[1] == 2, d[2] == 2, d[4] == 2)))
if s_chk.check() == unsat:
    answer_index_list.append(4)

print(answer_index_list)