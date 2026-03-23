from z3 import *

# Art historians: Farley=0, Garcia=1, Holden=2, Jiang=3
# Topics: lithographs=0, oil_paintings=1, sculptures=2, watercolors=3

# Position variables: pos_topic[topic] = lecture position (1-4)
pos_topic = [Int(f"pos_{t}") for t in ["lithographs", "oil_paintings", "sculptures", "watercolors"]]

# Position variables: pos_historian[historian] = lecture position (1-4)
pos_historian = [Int(f"pos_{h}") for h in ["Farley", "Garcia", "Holden", "Jiang"]]

# Base solver
solver = Solver()

# Domain constraints: positions are 1-4 and all distinct for topics
for i in range(4):
    solver.add(pos_topic[i] >= 1, pos_topic[i] <= 4)
solver.add(Distinct(*pos_topic))

# Domain constraints: positions are 1-4 and all distinct for historians
for i in range(4):
    solver.add(pos_historian[i] >= 1, pos_historian[i] <= 4)
solver.add(Distinct(*pos_historian))

# Topic-ordering constraints
# Oil paintings and watercolors before lithographs
solver.add(pos_topic[1] < pos_topic[0])  # oil_paintings < lithographs
solver.add(pos_topic[3] < pos_topic[0])  # watercolors < lithographs

# Farley's lecture before oil paintings lecture
solver.add(pos_historian[0] < pos_topic[1])  # Farley < oil_paintings

# Holden's lecture before Garcia's and Jiang's lectures
solver.add(pos_historian[2] < pos_historian[1])  # Holden < Garcia
solver.add(pos_historian[2] < pos_historian[3])  # Holden < Jiang

# Assignment constraint: each historian gives exactly one lecture on a topic
# Use binary assignment variables instead of integer indices to avoid type issues
assign = [[Bool(f"assign_{h}_{t}") for t in range(4)] for h in range(4)]

# Each historian assigned to exactly one topic
for h in range(4):
    solver.add(Sum([If(assign[h][t], 1, 0) for t in range(4)]) == 1)

# Each topic assigned to exactly one historian
for t in range(4):
    solver.add(Sum([If(assign[h][t], 1, 0) for h in range(4)]) == 1)

# Link assignment to positions: if historian h is assigned to topic t, then pos_historian[h] == pos_topic[t]
for h in range(4):
    for t in range(4):
        solver.add(Implies(assign[h][t], pos_historian[h] == pos_topic[t]))

# Answer choices (as logical statements)
# A: Farley < sculptures -> pos_historian[0] < pos_topic[2]
# B: Holden < lithographs -> pos_historian[2] < pos_topic[0]
# C: sculptures < Garcia -> pos_topic[2] < pos_historian[1]
# D: sculptures < Jiang -> pos_topic[2] < pos_historian[3]
# E: watercolors < Garcia -> pos_topic[3] < pos_historian[1]

answer_choices = [
    ("A", lambda: pos_historian[0] < pos_topic[2]),
    ("B", lambda: pos_historian[2] < pos_topic[0]),
    ("C", lambda: pos_topic[2] < pos_historian[1]),
    ("D", lambda: pos_topic[2] < pos_historian[3]),
    ("E", lambda: pos_topic[3] < pos_historian[1])
]

# Check each choice using proof by contradiction
answer_index_list = []
for idx, (label, statement) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the negation of the statement
    s_chk.add(Not(statement()))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)