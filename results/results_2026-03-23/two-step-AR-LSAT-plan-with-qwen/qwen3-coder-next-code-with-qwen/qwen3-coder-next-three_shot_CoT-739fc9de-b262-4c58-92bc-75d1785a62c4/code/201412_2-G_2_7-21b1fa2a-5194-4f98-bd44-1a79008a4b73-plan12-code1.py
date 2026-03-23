from z3 import *

# Art historians: Farley=0, Garcia=1, Holden=2, Jiang=3
# Topics: lithographs=0, oil_paintings=1, sculptures=2, watercolors=3

# Variables for historian lecture slots (1-4)
h = [Int(f"h_{i}") for i in range(4)]

# Variables for topic lecture slots (1-4)
t = [Int(f"t_{j}") for j in range(4)]

# Assignment matrix: assign[i][j] = True if historian i lectures on topic j
assign = [[Bool(f"assign_{i}_{j}") for j in range(4)] for i in range(4)]

# Base solver
solver = Solver()

# Each historian lectures on exactly one topic
for i in range(4):
    solver.add(Sum([If(assign[i][j], 1, 0) for j in range(4)]) == 1)

# Each topic is lectured by exactly one historian
for j in range(4):
    solver.add(Sum([If(assign[i][j], 1, 0) for i in range(4)]) == 1)

# Each historian gives exactly one lecture (distinct slots)
solver.add(Distinct(*h))
for i in range(4):
    solver.add(h[i] >= 1, h[i] <= 4)

# Each topic is covered in exactly one lecture (distinct slots)
solver.add(Distinct(*t))
for j in range(4):
    solver.add(t[j] >= 1, t[j] <= 4)

# Link assignment to slots: if historian i lectures on topic j, then h[i] == t[j]
for i in range(4):
    for j in range(4):
        solver.add(Implies(assign[i][j], h[i] == t[j]))

# Topic-order constraints: oil paintings and watercolors earlier than lithographs
solver.add(t[1] < t[0])  # oil_paintings < lithographs
solver.add(t[3] < t[0])  # watercolors < lithographs

# Speaker-order constraints: Farley before oil paintings
solver.add(h[0] < t[1])  # Farley < oil_paintings

# Holden before Garcia and Jiang
solver.add(h[2] < h[1])  # Holden < Garcia
solver.add(h[2] < h[3])  # Holden < Jiang

# Answer choices (as logical statements)
answer_choices = [
    h[0] < t[2],  # Farley before sculptures
    h[2] < t[0],  # Holden before lithographs
    t[2] < h[1],  # sculptures before Garcia
    t[2] < h[3],  # sculptures before Jiang
    t[3] < h[1]   # watercolors before Garcia
]

# Check each choice for necessity (negation UNSAT => must be true)
answer_index_list = []
for idx, stmt in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert negation of the statement
    s_chk.add(Not(stmt))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)