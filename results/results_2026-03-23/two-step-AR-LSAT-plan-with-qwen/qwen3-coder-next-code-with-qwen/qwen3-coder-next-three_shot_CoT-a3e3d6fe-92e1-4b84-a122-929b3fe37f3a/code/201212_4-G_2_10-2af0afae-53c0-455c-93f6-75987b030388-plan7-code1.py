from z3 import *

# Witness indices: 0-Franco, 1-Garcia, 2-Hong, 3-Iturbe, 4-Jackson
# Day indices: 0-Monday, 1-Tuesday, 2-Wednesday

d = [Int(f"d_{i}") for i in range(5)]

solver = Solver()

# Fixed constraint: Iturbe testifies on Wednesday
solver.add(d[3] == 2)

# Franco and Garcia do not testify on the same day
solver.add(d[0] != d[1])

# Exactly two witnesses testify on Tuesday
tuesday_count = Sum([If(d[i] == 1, 1, 0) for i in range(5)])
solver.add(tuesday_count == 2)

# Hong does not testify on Monday
solver.add(d[2] != 0)

# At least one witness testifies on Monday
monday_count = Sum([If(d[i] == 0, 1, 0) for i in range(5)])
solver.add(monday_count >= 1)

# Given hypothesis: Franco and Hong testify on the same day
solver.add(d[0] == d[2])

# Choices translation:
# 0: Franco testifies on Wednesday -> d[0] == 2
# 1: Garcia testifies on Monday -> d[1] == 0
# 2: Garcia testifies on Wednesday -> d[1] == 2
# 3: Hong testifies on Tuesday -> d[2] == 1
# 4: Iturbe is the only witness on Wednesday -> d[3] == 2 AND for all i != 3, d[i] != 2

forced_conditions = [False] * 5

# Check each choice
for j in range(5):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    if j == 0:
        # Choice 0 is false: Franco does NOT testify on Wednesday
        s_chk.add(d[0] != 2)
    elif j == 1:
        # Choice 1 is false: Garcia does NOT testify on Monday
        s_chk.add(d[1] != 0)
    elif j == 2:
        # Choice 2 is false: Garcia does NOT testify on Wednesday
        s_chk.add(d[1] != 2)
    elif j == 3:
        # Choice 3 is false: Hong does NOT testify on Tuesday
        s_chk.add(d[2] != 1)
    elif j == 4:
        # Choice 4 is false: Iturbe is NOT the only witness on Wednesday
        # This means either someone else also testifies on Wednesday, or Iturbe doesn't (but we know Iturbe must be on Wednesday)
        # So the negation is: there exists i != 3 such that d[i] == 2
        s_chk.add(Or(*[d[i] == 2 for i in range(5) if i != 3]))
    
    if s_chk.check() == unsat:
        forced_conditions[j] = True

# Find the index where forced_conditions is True
result_index = -1
for j in range(5):
    if forced_conditions[j]:
        result_index = j
        break

print(result_index)