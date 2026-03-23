from z3 import *

# Singer indices: Kammer=0, Lugo=1, Trillo=2, Waite=3, Yoshida=4, Zinn=5
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(*pos))

# Recorded constraints: Kammer (0) and Lugo (1) are recorded
# Fourth audition cannot be recorded → position 4 ≠ Kammer and ≠ Lugo
solver.add(pos[0] != 4, pos[1] != 4)

# Fifth audition must be recorded → exactly one of Kammer or Lugo is at position 5
# (since only two recorded auditions total, and both must be placed in non-4th positions)
solver.add(Or(
    And(pos[0] == 5, pos[1] != 5),
    And(pos[1] == 5, pos[0] != 5)
))

# Waite (3) must be earlier than both recorded auditions
solver.add(pos[3] < pos[0])
solver.add(pos[3] < pos[1])

# Kammer (0) before Trillo (2)
solver.add(pos[0] < pos[2])

# Zinn (5) before Yoshida (4)
solver.add(pos[5] < pos[4])

# Answer choices
choices = [
    ["Kammer", "Trillo", "Zinn", "Waite", "Lugo", "Yoshida"],
    ["Waite", "Kammer", "Yoshida", "Zinn", "Lugo", "Trillo"],
    ["Waite", "Lugo", "Kammer", "Trillo", "Zinn", "Yoshida"],
    ["Waite", "Zinn", "Kammer", "Trillo", "Lugo", "Yoshida"],
    ["Zinn", "Yoshida", "Waite", "Lugo", "Kammer", "Trillo"]
]

# Evaluate each choice
satisfiable_indices = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add position constraints for this specific ordering
    for i, singer in enumerate(choice):
        singer_idx = singers.index(singer)
        s_chk.add(pos[singer_idx] == i + 1)
    
    if s_chk.check() == sat:
        satisfiable_indices.append(idx)

print(satisfiable_indices)