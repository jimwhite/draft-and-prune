from z3 import *

# Topics: 0=lithographs, 1=oil paintings, 2=sculptures, 3=watercolors
# Historians: 0=Farley, 1=Garcia, 2=Holden, 3=Jiang

# Position variables for topics (1-4)
pos_topic = [Int(f"pos_topic_{t}") for t in range(4)]

# Position variables for historians (1-4)
pos_hist = [Int(f"pos_hist_{h}") for h in range(4)]

# Assignment variables: assign[h][t] = True if historian h gives lecture on topic t
assign = [[Bool(f"assign_{h}_{t}") for t in range(4)] for h in range(4)]

solver = Solver()

# Each topic has exactly one position (1-4) and all positions distinct
solver.add(Distinct(pos_topic))
for t in range(4):
    solver.add(pos_topic[t] >= 1, pos_topic[t] <= 4)

# Each historian has exactly one position (1-4) and all positions distinct
solver.add(Distinct(pos_hist))
for h in range(4):
    solver.add(pos_hist[h] >= 1, pos_hist[h] <= 4)

# Each historian is assigned exactly one topic
for h in range(4):
    solver.add(Sum([If(assign[h][t], 1, 0) for t in range(4)]) == 1)

# Each topic is assigned to exactly one historian
for t in range(4):
    solver.add(Sum([If(assign[h][t], 1, 0) for h in range(4)]) == 1)

# Link assignment to positions: if historian h gives topic t, then pos_hist[h] == pos_topic[t]
for h in range(4):
    for t in range(4):
        solver.add(Implies(assign[h][t], pos_hist[h] == pos_topic[t]))

# Ordering constraints
# Oil paintings (1) and watercolors (3) before lithographs (0)
solver.add(pos_topic[1] < pos_topic[0])  # oil < lith
solver.add(pos_topic[3] < pos_topic[0])  # water < lith

# Farley's lecture before oil paintings lecture
solver.add(pos_hist[0] < pos_topic[1])  # Farley < oil

# Holden's lecture before Garcia's and Jiang's lectures
solver.add(pos_hist[2] < pos_hist[1])  # Holden < Garcia
solver.add(pos_hist[2] < pos_hist[3])  # Holden < Jiang

# Answer choices (negations to test for "must be true")
answer_choices = [
    # 0: Farley < Sculptures (2)
    lambda s: s.add(pos_hist[0] >= pos_topic[2]),
    # 1: Holden < Lithographs (0)
    lambda s: s.add(pos_hist[2] >= pos_topic[0]),
    # 2: Sculptures (2) < Garcia (1)
    lambda s: s.add(pos_topic[2] >= pos_hist[1]),
    # 3: Sculptures (2) < Jiang (3)
    lambda s: s.add(pos_topic[2] >= pos_hist[3]),
    # 4: Watercolors (3) < Garcia (1)
    lambda s: s.add(pos_topic[3] >= pos_hist[1])
]

answer_index_list = []
for idx, add_negation in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add negation of the statement
    add_negation(s_chk)
    
    # If UNSAT, then the original statement must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)