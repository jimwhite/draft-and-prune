from z3 import *

# Art historians indices: 0-Farley, 1-Garcia, 2-Holden, 3-Jiang
# Topics indices: 0-lithographs, 1-oil paintings, 2-sculptures, 3-watercolors

# Position variables for historians (1-4)
pos_h = [Int(f"pos_h_{i}") for i in range(4)]

# Position variables for topics (1-4)
topic_pos = [Int(f"pos_t_{j}") for j in range(4)]

# Assignment variables: assign[i][j] = 1 if historian i gives lecture on topic j
assign = [[Bool(f"assign_{i}_{j}") for j in range(4)] for i in range(4)]

# Base solver
solver = Solver()

# Each historian has a unique position (1-4)
solver.add(Distinct(*pos_h))
for i in range(4):
    solver.add(pos_h[i] >= 1, pos_h[i] <= 4)

# Each topic has a unique position (1-4)
solver.add(Distinct(*topic_pos))
for j in range(4):
    solver.add(topic_pos[j] >= 1, topic_pos[j] <= 4)

# Each historian assigned to exactly one topic
for i in range(4):
    solver.add(Sum([If(assign[i][j], 1, 0) for j in range(4)]) == 1)

# Each topic assigned to exactly one historian
for j in range(4):
    solver.add(Sum([If(assign[i][j], 1, 0) for i in range(4)]) == 1)

# Link assignment with positions: if assign[i][j] is true, then pos_h[i] == topic_pos[j]
for i in range(4):
    for j in range(4):
        solver.add(Implies(assign[i][j], pos_h[i] == topic_pos[j]))

# Topic-order constraints: oil paintings and watercolors before lithographs
solver.add(topic_pos[1] < topic_pos[0])  # oil paintings before lithographs
solver.add(topic_pos[3] < topic_pos[0])  # watercolors before lithographs

# Historian-order constraints:
# Farley's lecture earlier than oil paintings lecture
solver.add(pos_h[0] < topic_pos[1])  # Farley before oil paintings

# Holden's lecture earlier than both Garcia's and Jiang's lectures
solver.add(pos_h[2] < pos_h[1])  # Holden before Garcia
solver.add(pos_h[2] < pos_h[3])  # Holden before Jiang

# Answer choices (negations to test for "must be true")
answer_choices = [
    # (A) Farley's lecture earlier than sculptures lecture
    lambda: pos_h[0] < topic_pos[2],
    # (B) Holden's lecture earlier than lithographs lecture
    lambda: pos_h[2] < topic_pos[0],
    # (C) sculptures lecture earlier than Garcia's lecture
    lambda: topic_pos[2] < pos_h[1],
    # (D) sculptures lecture earlier than Jiang's lecture
    lambda: topic_pos[2] < pos_h[3],
    # (E) watercolors lecture earlier than Garcia's lecture
    lambda: topic_pos[3] < pos_h[1]
]

answer_index_list = []
for idx, constraint_func in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add negation of the constraint
    s_chk.add(Not(constraint_func()))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)