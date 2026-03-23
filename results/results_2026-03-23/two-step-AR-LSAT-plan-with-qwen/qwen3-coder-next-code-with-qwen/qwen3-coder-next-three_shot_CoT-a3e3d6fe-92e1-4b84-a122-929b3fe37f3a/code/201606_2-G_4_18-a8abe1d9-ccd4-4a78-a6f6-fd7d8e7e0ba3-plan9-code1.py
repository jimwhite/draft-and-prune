from z3 import *

# Singer indices: Kammer=0, Lugo=1, Trillo=2, Waite=3, Yoshida=4, Zinn=5
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
singer_idx = {name: i for i, name in enumerate(singers)}

# Position variables (1-indexed)
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(*pos))

# Recording constraints
# Recorded: Kammer (0) and Lugo (1)
# 4th audition cannot be recorded → Kammer and Lugo not in position 4
solver.add(pos[0] != 4, pos[1] != 4)
# 5th audition must be recorded → exactly one of Kammer or Lugo is in position 5
solver.add(Or(And(pos[0] == 5, pos[1] != 5), And(pos[0] != 5, pos[1] == 5)))

# Ordering constraints
# Waite (3) earlier than both recorded auditions: pos[3] < pos[0] and pos[3] < pos[1]
solver.add(pos[3] < pos[0])
solver.add(pos[3] < pos[1])

# Kammer (0) earlier than Trillo (2)
solver.add(pos[0] < pos[2])

# Zinn (5) earlier than Yoshida (4)
solver.add(pos[5] < pos[4])

# Answer choices
answer_choices = [
    ["Kammer", "Trillo", "Zinn", "Waite", "Lugo", "Yoshida"],
    ["Waite", "Kammer", "Yoshida", "Zinn", "Lugo", "Trillo"],
    ["Waite", "Lugo", "Kammer", "Trillo", "Zinn", "Yoshida"],
    ["Waite", "Zinn", "Kammer", "Trillo", "Lugo", "Yoshida"],
    ["Zinn", "Yoshida", "Waite", "Lugo", "Kammer", "Trillo"]
]

# Check each choice
answer_index_list = []
for idx, order in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add position constraints based on the order
    for pos_idx, singer in enumerate(order):
        s_chk.add(pos[singer_idx[singer]] == pos_idx + 1)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Print the smallest index (only one correct)
print(min(answer_index_list) if answer_index_list else -1)