from z3 import *

# Art historians: Farley=0, Garcia=1, Holden=2, Jiang=3
# Topics: lithographs=0, oil_paintings=1, sculptures=2, watercolors=3

# Binary assignment variables: assign[i][j] = 1 if historian i gives lecture on topic j
assign = [[Bool(f"assign_{i}_{j}") for j in range(4)] for i in range(4)]

# Position variables: h_pos[i] = position of historian i's lecture (1-4), t_pos[j] = position of topic j's lecture (1-4)
h_pos = [Int(f"h_pos_{i}") for i in range(4)]
t_pos = [Int(f"t_pos_{j}") for j in range(4)]

solver = Solver()

# Each historian gives exactly one topic
for i in range(4):
    solver.add(Sum([If(assign[i][j], 1, 0) for j in range(4)]) == 1)

# Each topic is given by exactly one historian
for j in range(4):
    solver.add(Sum([If(assign[i][j], 1, 0) for i in range(4)]) == 1)

# Link h_pos and t_pos: if assign[i][j] is true, then h_pos[i] == t_pos[j]
for i in range(4):
    for j in range(4):
        solver.add(Implies(assign[i][j], h_pos[i] == t_pos[j]))

# Each historian's position is between 1 and 4
for i in range(4):
    solver.add(h_pos[i] >= 1, h_pos[i] <= 4)

# Each topic's position is between 1 and 4
for j in range(4):
    solver.add(t_pos[j] >= 1, t_pos[j] <= 4)

# All historian positions are distinct
solver.add(Distinct(*h_pos))

# All topic positions are distinct
solver.add(Distinct(*t_pos))

# Topic ordering constraints:
# Oil paintings and watercolors lectures are both earlier than lithographs
solver.add(t_pos[1] < t_pos[0])  # oil_paintings < lithographs
solver.add(t_pos[3] < t_pos[0])  # watercolors < lithographs

# Farley's lecture is earlier than oil paintings
solver.add(h_pos[0] < t_pos[1])  # Farley < oil_paintings

# Holden's lecture is earlier than both Garcia's and Jiang's
solver.add(h_pos[2] < h_pos[1])  # Holden < Garcia
solver.add(h_pos[2] < h_pos[3])  # Holden < Jiang

# Answer choices (as logical statements):
# 0: Farley's lecture is earlier than the sculptures lecture → h_pos[0] < t_pos[2]
# 1: Holden's lecture is earlier than the lithographs lecture → h_pos[2] < t_pos[0]
# 2: The sculptures lecture is earlier than Garcia's lecture → t_pos[2] < h_pos[1]
# 3: The sculptures lecture is earlier than Jiang's lecture → t_pos[2] < h_pos[3]
# 4: The watercolors lecture is earlier than Garcia's lecture → t_pos[3] < h_pos[1]

answer_choices = [
    lambda: h_pos[0] < t_pos[2],  # Farley earlier than sculptures
    lambda: h_pos[2] < t_pos[0],  # Holden earlier than lithographs
    lambda: t_pos[2] < h_pos[1],  # sculptures earlier than Garcia
    lambda: t_pos[2] < h_pos[3],  # sculptures earlier than Jiang
    lambda: t_pos[3] < h_pos[1],  # watercolors earlier than Garcia
]

# Check which statements must be true (negation is UNSAT)
answer_index_list = []
for idx, stmt in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add negation of the statement
    s_chk.add(Not(stmt()))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)