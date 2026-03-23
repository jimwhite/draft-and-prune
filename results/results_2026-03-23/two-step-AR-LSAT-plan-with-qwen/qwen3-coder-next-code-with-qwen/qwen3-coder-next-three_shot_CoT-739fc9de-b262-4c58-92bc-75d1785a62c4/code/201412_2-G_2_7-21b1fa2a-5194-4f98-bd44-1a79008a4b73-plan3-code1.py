from z3 import *

# Art historians: Farley=0, Garcia=1, Holden=2, Jiang=3
# Topics: lithographs=0, oil paintings=1, sculptures=2, watercolors=3

# Position variables for historians (1-4)
pos_H = [Int(f"pos_H_{h}") for h in range(4)]

# Position variables for topics (1-4)
topic_pos = [Int(f"topic_pos_{t}") for t in range(4)]

# Assignment variables: assign[h][t] = True if historian h gives lecture on topic t
assign = [[Bool(f"assign_{h}_{t}") for t in range(4)] for h in range(4)]

# Base solver
solver = Solver()

# Each historian gives exactly one lecture (each historian assigned to exactly one topic)
for h in range(4):
    solver.add(Sum([If(assign[h][t], 1, 0) for t in range(4)]) == 1)

# Each topic is covered by exactly one historian
for t in range(4):
    solver.add(Sum([If(assign[h][t], 1, 0) for h in range(4)]) == 1)

# Link assignment to positions: historian h gives topic t lecture iff pos_H[h] == topic_pos[t]
for h in range(4):
    for t in range(4):
        solver.add(Implies(assign[h][t], pos_H[h] == topic_pos[t]))
        solver.add(Implies(pos_H[h] == topic_pos[t], assign[h][t]))

# Each historian gives exactly one lecture (positions distinct)
solver.add(Distinct(*pos_H))

# Each topic is covered exactly once (topic positions distinct)
solver.add(Distinct(*topic_pos))

# Domain constraints: positions between 1 and 4
for h in range(4):
    solver.add(pos_H[h] >= 1, pos_H[h] <= 4)
for t in range(4):
    solver.add(topic_pos[t] >= 1, topic_pos[t] <= 4)

# Topic ordering constraints
## Oil paintings and watercolors both earlier than lithographs
solver.add(topic_pos[1] < topic_pos[0])  # oil paintings < lithographs
solver.add(topic_pos[3] < topic_pos[0])  # watercolors < lithographs

# Farley's lecture earlier than oil paintings
solver.add(pos_H[0] < topic_pos[1])  # Farley < oil paintings

# Holden's lecture earlier than both Garcia's and Jiang's
solver.add(pos_H[2] < pos_H[1])  # Holden < Garcia
solver.add(pos_H[2] < pos_H[3])  # Holden < Jiang

# Answer choices (as logical statements that must be true)
# A: Farley's lecture earlier than sculptures => pos_H[0] < topic_pos[2]
# B: Holden's lecture earlier than lithographs => pos_H[2] < topic_pos[0]
# C: Sculptures earlier than Garcia's => topic_pos[2] < pos_H[1]
# D: Sculptures earlier than Jiang's => topic_pos[2] < pos_H[3]
# E: Watercolors earlier than Garcia's => topic_pos[3] < pos_H[1]

answer_conditions = [
    lambda: pos_H[0] < topic_pos[2],  # A
    lambda: pos_H[2] < topic_pos[0],  # B
    lambda: topic_pos[2] < pos_H[1],  # C
    lambda: topic_pos[2] < pos_H[3],  # D
    lambda: topic_pos[3] < pos_H[1]   # E
]

must_be_true_indices = []

for i, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the negation of the condition (i.e., the statement is false)
    s_chk.add(Not(cond()))
    
    # If UNSAT, then the condition must be true in all models
    if s_chk.check() == unsat:
        must_be_true_indices.append(i)

print(must_be_true_indices)