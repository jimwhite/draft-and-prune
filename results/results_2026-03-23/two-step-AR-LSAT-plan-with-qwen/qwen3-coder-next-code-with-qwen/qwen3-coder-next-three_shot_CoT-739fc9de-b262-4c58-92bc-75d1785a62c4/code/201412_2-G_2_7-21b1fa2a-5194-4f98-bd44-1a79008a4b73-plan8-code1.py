from z3 import *

# Art historians: Farley=0, Garcia=1, Holden=2, Jiang=3
# Topics: lithographs=0, oil_paintings=1, sculptures=2, watercolors=3

# Position variables: hist[h] = lecture position (1-4) of historian h
hist = [Int(f"hist_{h}") for h in range(4)]

# Position variables: topic[t] = lecture position (1-4) of topic t
topic = [Int(f"topic_{t}") for t in range(4)]

# Assignment variables: assigned[h][t] = True if historian h gives lecture on topic t
assigned = [[Bool(f"assigned_{h}_{t}") for t in range(4)] for h in range(4)]

solver = Solver()

# Each historian gives exactly one topic
for h in range(4):
    solver.add(Sum([If(assigned[h][t], 1, 0) for t in range(4)]) == 1)

# Each topic is given by exactly one historian
for t in range(4):
    solver.add(Sum([If(assigned[h][t], 1, 0) for h in range(4)]) == 1)

# Relate hist and topic via assignment: hist[h] == topic[t] iff assigned[h][t]
for h in range(4):
    for t in range(4):
        solver.add(Implies(assigned[h][t], hist[h] == topic[t]))
        solver.add(Implies(hist[h] == topic[t], assigned[h][t]))

# Domain constraints: positions are 1-4 and distinct
solver.add(Distinct(*hist))
solver.add(Distinct(*topic))
for h in range(4):
    solver.add(hist[h] >= 1, hist[h] <= 4)
for t in range(4):
    solver.add(topic[t] >= 1, topic[t] <= 4)

# Ordering constraints
# Oil paintings and watercolors lectures are both earlier than lithographs
solver.add(topic[1] < topic[0])  # oil < litho
solver.add(topic[3] < topic[0])  # water < litho

# Farley's lecture is earlier than oil paintings
solver.add(hist[0] < topic[1])  # Farley < oil

# Holden's lecture is earlier than both Garcia's and Jiang's
solver.add(hist[2] < hist[1])  # Holden < Garcia
solver.add(hist[2] < hist[3])  # Holden < Jiang

# Answer choices (indices)
# A: Farley's lecture earlier than sculptures → hist[0] < topic[2]
# B: Holden's lecture earlier than lithographs → hist[2] < topic[0]
# C: sculptures earlier than Garcia's lecture → topic[2] < hist[1]
# D: sculptures earlier than Jiang's lecture → topic[2] < hist[3]
# E: watercolors earlier than Garcia's lecture → topic[3] < hist[1]

answer_choices = [
    lambda: hist[0] < topic[2],  # A
    lambda: hist[2] < topic[0],  # B
    lambda: topic[2] < hist[1],  # C
    lambda: topic[2] < hist[3],  # D
    lambda: topic[3] < hist[1]   # E
]

# Check each choice by negating and testing UNSAT
must_be_true_indices = []
for idx, constraint_fn in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add negation of the constraint
    s_chk.add(Not(constraint_fn()))
    
    if s_chk.check() == unsat:
        must_be_true_indices.append(idx)

# Print the index of the must-be-true choice
print(must_be_true_indices)