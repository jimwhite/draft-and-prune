from z3 import *

# Historian indices: Farley=0, Garcia=1, Holden=2, Jiang=3
# Topic indices: lithographs=0, oil paintings=1, sculptures=2, watercolors=3

# For each slot (0-3 representing positions 1-4), create Boolean variables
h_slot = [[Bool(f"h_{i}_{s}") for s in range(4)] for i in range(4)]
t_slot = [[Bool(f"t_{j}_{s}") for s in range(4)] for j in range(4)]

solver = Solver()

# Each historian appears exactly once
for i in range(4):
    solver.add(Or([h_slot[i][s] for s in range(4)]))
    for s1 in range(4):
        for s2 in range(s1+1, 4):
            solver.add(Not(And(h_slot[i][s1], h_slot[i][s2])))

# Each slot has exactly one historian
for s in range(4):
    solver.add(Or([h_slot[i][s] for i in range(4)]))
    for i1 in range(4):
        for i2 in range(i1+1, 4):
            solver.add(Not(And(h_slot[i1][s], h_slot[i2][s])))

# Each topic appears exactly once
for j in range(4):
    solver.add(Or([t_slot[j][s] for s in range(4)]))
    for s1 in range(4):
        for s2 in range(s1+1, 4):
            solver.add(Not(And(t_slot[j][s1], t_slot[j][s2])))

# Each slot has exactly one topic
for s in range(4):
    solver.add(Or([t_slot[j][s] for j in range(4)]))
    for j1 in range(4):
        for j2 in range(j1+1, 4):
            solver.add(Not(And(t_slot[j1][s], t_slot[j2][s])))

# Compute historian positions: pos_h[i] = slot index + 1
pos_h = [Int(f"pos_h_{i}") for i in range(4)]
for i in range(4):
    solver.add(pos_h[i] == Sum([If(h_slot[i][s], s+1, 0) for s in range(4)]))

# Compute topic positions: t_pos[j] = slot index + 1
t_pos = [Int(f"t_pos_{j}") for j in range(4)]
for j in range(4):
    solver.add(t_pos[j] == Sum([If(t_slot[j][s], s+1, 0) for s in range(4)]))

# Ordering constraints
# oil paintings (1) and watercolors (3) must both be earlier than lithographs (0)
solver.add(t_pos[1] < t_pos[0])
solver.add(t_pos[3] < t_pos[0])

# Farley's (0) lecture earlier than oil paintings (1)
solver.add(pos_h[0] < t_pos[1])

# Holden's (2) earlier than Garcia's (1) and Jiang's (3)
solver.add(pos_h[2] < pos_h[1])
solver.add(pos_h[2] < pos_h[3])

# Answer choices (as logical statements)
answer_choices = [
    ("Farley earlier than sculptures", pos_h[0] < t_pos[2]),  # A
    ("Holden earlier than lithographs", pos_h[2] < t_pos[0]),  # B
    ("sculptures earlier than Garcia", t_pos[2] < pos_h[1]),  # C
    ("sculptures earlier than Jiang", t_pos[2] < pos_h[3]),  # D
    ("watercolors earlier than Garcia", t_pos[3] < pos_h[1])  # E
]

# Check which statements must be true (negation leads to UNSAT)
answer_index_list = []
for idx, (_, stmt) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    # Add negation of the statement
    s_chk.add(Not(stmt))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)