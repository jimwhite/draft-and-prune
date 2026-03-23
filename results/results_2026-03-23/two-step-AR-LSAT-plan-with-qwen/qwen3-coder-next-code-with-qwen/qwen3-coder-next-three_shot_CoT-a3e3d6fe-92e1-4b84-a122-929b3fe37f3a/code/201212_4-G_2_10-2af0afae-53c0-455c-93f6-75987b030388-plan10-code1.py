from z3 import *

# Witness indices: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
witnesses = ["Franco", "Garcia", "Hong", "Iturbe", "Jackson"]
day = [Int(f"day_{w}") for w in witnesses]

# Base solver
solver = Solver()

# Domain constraints: each witness tests on Monday (0), Tuesday (1), or Wednesday (2)
for d in day:
    solver.add(d >= 0, d <= 2)

# Iturbe testifies on Wednesday
solver.add(day[3] == 2)

# Exactly two witnesses testify on Tuesday
solver.add(Sum([If(d == 1, 1, 0) for d in day]) == 2)

# At least one witness testifies on Monday
solver.add(Sum([If(d == 0, 1, 0) for d in day]) >= 1)

# Franco and Garcia do not testify on the same day
solver.add(day[0] != day[1])

# Hong does not testify on Monday
solver.add(day[2] != 0)

# Given assumption: Franco and Hong testify on the same day
solver.add(day[0] == day[2])

# Answer choices (as conditions that must be true)
# A: Franco is scheduled to testify on Wednesday -> day[0] == 2
# B: Garcia is scheduled to testify on Monday -> day[1] == 0
# C: Garcia is scheduled to testify on Wednesday -> day[1] == 2
# D: Hong is scheduled to testify on Tuesday -> day[2] == 1
# E: Iturbe is the only witness scheduled to testify on Wednesday -> 
#    day[3] == 2 AND for all other witnesses w != 3, day[w] != 2

forced_condition_indices = []

# Check A: Franco on Wednesday
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(day[0] != 2)  # Negate A
if s_chk.check() == unsat:
    forced_condition_indices.append(0)

# Check B: Garcia on Monday
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(day[1] != 0)  # Negate B
if s_chk.check() == unsat:
    forced_condition_indices.append(1)

# Check C: Garcia on Wednesday
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(day[1] != 2)  # Negate C
if s_chk.check() == unsat:
    forced_condition_indices.append(2)

# Check D: Hong on Tuesday
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(day[2] != 1)  # Negate D
if s_chk.check() == unsat:
    forced_condition_indices.append(3)

# Check E: Iturbe is the only witness on Wednesday
s_chk = Solver()
s_chk.add(solver.assertions())
# Negate E: either Iturbe not on Wednesday (already fixed, so always false) OR at least one other witness on Wednesday
# Since Iturbe is fixed to Wednesday, negation is: some other witness also on Wednesday
s_chk.add(Or(day[0] == 2, day[1] == 2, day[2] == 2, day[4] == 2))
if s_chk.check() == unsat:
    forced_condition_indices.append(4)

print(forced_condition_indices)