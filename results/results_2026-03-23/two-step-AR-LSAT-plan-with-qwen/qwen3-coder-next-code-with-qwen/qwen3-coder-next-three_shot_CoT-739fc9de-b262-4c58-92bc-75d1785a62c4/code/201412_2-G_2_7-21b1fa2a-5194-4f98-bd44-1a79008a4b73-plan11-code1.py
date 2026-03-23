from z3 import *

# Historian indices: 0-Farley, 1-Garcia, 2-Holden, 3-Jiang
# Topic indices: 0-lithographs, 1-oil paintings, 2-sculptures, 3-watercolors

# Slot variables: for each slot (1-4), which historian and topic
h = [Int(f"h_{s}") for s in range(1, 5)]  # historian per slot
t = [Int(f"t_{s}") for s in range(1, 5)]  # topic per slot

solver = Solver()

# Each historian appears exactly once
solver.add(Distinct(h))

# Each topic appears exactly once
solver.add(Distinct(t))

# Domain constraints: historians 0-3, topics 0-3
for i in range(4):
    solver.add(h[i] >= 0, h[i] <= 3)
    solver.add(t[i] >= 0, t[i] <= 3)

# Topic-based ordering constraints
# oil paintings (1) and watercolors (3) must both be earlier than lithographs (0)
solver.add(t[1] < t[0])  # oil paintings before lithographs
solver.add(t[3] < t[0])  # watercolors before lithographs

# Farley (0) must be earlier than oil paintings lecture
solver.add(h[0] < t[1])  # Farley before oil paintings

# Holden (2) must be earlier than Garcia (1) and Jiang (3)
solver.add(h[2] < h[1])  # Holden before Garcia
solver.add(h[2] < h[3])  # Holden before Jiang

# Answer choices (as logical statements)
# A: Farley earlier than sculptures → h[0] < t[2]
# B: Holden earlier than lithographs → h[2] < t[0]
# C: sculptures earlier than Garcia → t[2] < h[1]
# D: sculptures earlier than Jiang → t[2] < h[3]
# E: watercolors earlier than Garcia → t[3] < h[1]

answer_choices = [
    ("h[0] < t[2]", lambda: h[0] < t[2]),      # A
    ("h[2] < t[0]", lambda: h[2] < t[0]),      # B
    ("t[2] < h[1]", lambda: t[2] < h[1]),      # C
    ("t[2] < h[3]", lambda: t[2] < h[3]),      # D
    ("t[3] < h[1]", lambda: t[3] < h[1])       # E
]

answer_index_list = []

for idx, (desc, stmt) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Negate the statement
    s_chk.add(Not(stmt()))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)