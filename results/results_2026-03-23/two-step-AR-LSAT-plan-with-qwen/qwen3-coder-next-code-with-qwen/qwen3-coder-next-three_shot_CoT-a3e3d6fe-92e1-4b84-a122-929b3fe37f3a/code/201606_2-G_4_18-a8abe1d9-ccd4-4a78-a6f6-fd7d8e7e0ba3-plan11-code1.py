from z3 import *

# Singer indices: Kammer=0, Lugo=1, Trillo=2, Waite=3, Yoshida=4, Zinn=5
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
recording = {0, 1}  # Kammer and Lugo are recorded

# Position variables (1-indexed)
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(pos))

# Recording constraints
# Fourth audition cannot be recorded → position 4 must be held by non-recorded singer (indices 2,3,4,5)
solver.add(And(*[pos[i] != 4 for i in recording]))

# Fifth audition must be recorded → position 5 must be held by a recorded singer (index 0 or 1)
solver.add(Or(pos[0] == 5, pos[1] == 5))

# Order constraints
# Waite (3) must be earlier than both recorded auditions (0 and 1)
solver.add(pos[3] < pos[0])
solver.add(pos[3] < pos[1])

# Kammer (0) earlier than Trillo (2)
solver.add(pos[0] < pos[2])

# Zinn (5) earlier than Yoshida (4)
solver.add(pos[5] < pos[4])

# Answer choices
choices = [
    ["Kammer", "Trillo", "Zinn", "Waite", "Lugo", "Yoshida"],
    ["Waite", "Kammer", "Yoshida", "Zinn", "Lugo", "Trillo"],
    ["Waite", "Lugo", "Kammer", "Trillo", "Zinn", "Yoshida"],
    ["Waite", "Zinn", "Kammer", "Trillo", "Lugo", "Yoshida"],
    ["Zinn", "Yoshida", "Waite", "Lugo", "Kammer", "Trillo"]
]

# Check each choice
answer_index_list = []
for idx, order in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Map singer names to indices and assert positions
    for i, name in enumerate(order):
        s_idx = singers.index(name)
        s_chk.add(pos[s_idx] == i + 1)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)