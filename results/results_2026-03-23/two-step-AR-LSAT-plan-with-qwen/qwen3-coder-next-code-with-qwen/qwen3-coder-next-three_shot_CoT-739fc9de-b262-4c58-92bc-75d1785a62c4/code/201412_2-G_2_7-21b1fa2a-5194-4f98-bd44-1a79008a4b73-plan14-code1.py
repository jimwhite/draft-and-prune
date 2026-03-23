from z3 import *

# Art historians: 0-Farley, 1-Garcia, 2-Holden, 3-Jiang
# Topics: 0-lithographs, 1-oil paintings, 2-sculptures, 3-watercolors

# Position variables for historians (1-4)
pos_h = [Int(f"pos_h_{i}") for i in range(4)]

# Position variables for topics (1-4)
pos_t = [Int(f"pos_t_{t}") for t in range(4)]

# Assignment variables: assign[i][t] = True if historian i gives lecture on topic t
assign = [[Bool(f"assign_{i}_{t}") for t in range(4)] for i in range(4)]

# Base solver
solver = Solver()

# Each historian gives exactly one lecture
for i in range(4):
    solver.add(Sum([If(assign[i][t], 1, 0) for t in range(4)]) == 1)

# Each topic is given by exactly one historian
for t in range(4):
    solver.add(Sum([If(assign[i][t], 1, 0) for i in range(4)]) == 1)

# Historian positions are distinct and between 1-4
solver.add(Distinct(*pos_h))
for i in range(4):
    solver.add(pos_h[i] >= 1, pos_h[i] <= 4)

# Topic positions are distinct and between 1-4
solver.add(Distinct(*pos_t))
for t in range(4):
    solver.add(pos_t[t] >= 1, pos_t[t] <= 4)

# Link assignment to positions: if historian i gives topic t, then pos_t[t] == pos_h[i]
for i in range(4):
    for t in range(4):
        solver.add(Implies(assign[i][t], pos_t[t] == pos_h[i]))

# Order constraints
## oil paintings and watercolors before lithographs
solver.add(pos_t[1] < pos_t[0])  # oil paintings < lithographs
solver.add(pos_t[3] < pos_t[0])  # watercolors < lithographs

## Farley's lecture before oil paintings
solver.add(pos_h[0] < pos_t[1])  # Farley < oil paintings

## Holden's lecture before Garcia's and Jiang's
solver.add(pos_h[2] < pos_h[1])  # Holden < Garcia
solver.add(pos_h[2] < pos_h[3])  # Holden < Jiang

# Answer choices (as conditions that must be true)
# 0: Farley's lecture earlier than sculptures -> pos_h[0] < pos_t[2]
# 1: Holden's lecture earlier than lithographs -> pos_h[2] < pos_t[0]
# 2: sculptures earlier than Garcia's -> pos_t[2] < pos_h[1]
# 3: sculptures earlier than Jiang's -> pos_t[2] < pos_h[3]
# 4: watercolors earlier than Garcia's -> pos_t[3] < pos_h[1]

answer_conditions = [
    pos_h[0] < pos_t[2],  # Farley < sculptures
    pos_h[2] < pos_t[0],  # Holden < lithographs
    pos_t[2] < pos_h[1],  # sculptures < Garcia
    pos_t[2] < pos_h[3],  # sculptures < Jiang
    pos_t[3] < pos_h[1]   # watercolors < Garcia
]

answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add negation of the condition
    s_chk.add(Not(cond))
    
    # If UNSAT, then the condition must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)