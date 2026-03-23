from z3 import *

# Singer indices: Kammer=0, Lugo=1, Trillo=2, Waite=3, Yoshida=4, Zinn=5
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Distinctness constraint: all positions are distinct (1 to 6)
solver.add(Distinct(*pos))
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)

# Recording constraints: Kammer (0) and Lugo (1) are the only recorded auditions
# Fourth audition is unrecorded → position 4 not equal to pos[0] or pos[1]
solver.add(pos[0] != 4, pos[1] != 4)
# Fifth audition is recorded → position 5 equals pos[0] or pos[1]
solver.add(Or(pos[0] == 5, pos[1] == 5))

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

# Check each choice
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert positions based on the choice order
    for i, singer in enumerate(choice):
        singer_idx = singers.index(singer)
        s_chk.add(pos[singer_idx] == i + 1)
    
    if s_chk.check() == sat:
        print(idx)
        break