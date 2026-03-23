from z3 import *

# Art historians indices: 0-Farley, 1-Garcia, 2-Holden, 3-Jiang
# Topics indices: 0-lithographs, 1-oil paintings, 2-sculptures, 3-watercolors

# h_pos[h] = position (1-4) of historian h's lecture
h_pos = [Int(f"h_pos_{i}") for i in range(4)]

# t_who[t] = historian index who gives lecture on topic t
t_who = [Int(f"t_who_{j}") for j in range(4)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-4, all distinct for historians
for i in range(4):
    solver.add(h_pos[i] >= 1, h_pos[i] <= 4)
solver.add(Distinct(*h_pos))

# Topic assignment constraints: each topic assigned to exactly one historian
for j in range(4):
    solver.add(t_who[j] >= 0, t_who[j] <= 3)
solver.add(Distinct(*t_who))

# Link historian positions and topic assignments:
# For each topic j, if t_who[j] = i, then the position of topic j is h_pos[i]
# We'll use this by adding constraints that relate positions and assignments
for j in range(4):
    # For each topic, its position equals the historian's position who teaches it
    pos_constraints = []
    for i in range(4):
        # If t_who[j] == i, then topic_j_pos == h_pos[i]
        pos_constraints.append(Implies(t_who[j] == i, And(
            # Define topic position variable implicitly via historian position
            True  # We'll handle this differently: use h_pos[t_who[j]] conceptually
        )))
    # Instead, we'll directly use h_pos[t_who[j]] in ordering constraints
    # But Z3 doesn't support array indexing with expressions directly for Int variables
    # So we'll use a different approach: create topic position variables

# Alternative approach: Create topic position variables directly
t_pos = [Int(f"t_pos_{j}") for j in range(4)]

# Domain constraints for topic positions
for j in range(4):
    solver.add(t_pos[j] >= 1, t_pos[j] <= 4)
solver.add(Distinct(*t_pos))

# Link historian positions and topic assignments:
# Each historian gives exactly one topic, each topic assigned to exactly one historian
assigned = [[Bool(f"assigned_{i}_{j}") for j in range(4)] for i in range(4)]

# Each historian assigned to exactly one topic
for i in range(4):
    solver.add(Sum([If(assigned[i][j], 1, 0) for j in range(4)]) == 1)

# Each topic assigned to exactly one historian
for j in range(4):
    solver.add(Sum([If(assigned[i][j], 1, 0) for i in range(4)]) == 1)

# Link positions: if historian i gives topic j, then h_pos[i] == t_pos[j]
for i in range(4):
    for j in range(4):
        solver.add(Implies(assigned[i][j], h_pos[i] == t_pos[j]))

# Topic ordering constraints:
# oil paintings (1) and watercolors (3) earlier than lithographs (0)
solver.add(t_pos[1] < t_pos[0])  # oil paintings before lithographs
solver.add(t_pos[3] < t_pos[0])  # watercolors before lithographs

# Farley (0) earlier than oil paintings (1)
solver.add(h_pos[0] < t_pos[1])

# Holden (2) earlier than Garcia (1) and Jiang (3)
solver.add(h_pos[2] < h_pos[1])  # Holden before Garcia
solver.add(h_pos[2] < h_pos[3])  # Holden before Jiang

# Answer choices (convert to constraints that must be true)
answer_choices = [
    # Farley's lecture earlier than sculptures (2): h_pos[0] < t_pos[2]
    lambda: h_pos[0] < t_pos[2],
    # Holden's lecture earlier than lithographs (0): h_pos[2] < t_pos[0]
    lambda: h_pos[2] < t_pos[0],
    # Sculptures (2) earlier than Garcia (1): t_pos[2] < h_pos[1]
    lambda: t_pos[2] < h_pos[1],
    # Sculptures (2) earlier than Jiang (3): t_pos[2] < h_pos[3]
    lambda: t_pos[2] < h_pos[3],
    # Watercolors (3) earlier than Garcia (1): t_pos[3] < h_pos[1]
    lambda: t_pos[3] < h_pos[1]
]

# Check each answer choice using proof by contradiction
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add negation of the choice
    s_chk.add(Not(choice()))
    
    # If UNSAT, then the choice must be true in all models
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)