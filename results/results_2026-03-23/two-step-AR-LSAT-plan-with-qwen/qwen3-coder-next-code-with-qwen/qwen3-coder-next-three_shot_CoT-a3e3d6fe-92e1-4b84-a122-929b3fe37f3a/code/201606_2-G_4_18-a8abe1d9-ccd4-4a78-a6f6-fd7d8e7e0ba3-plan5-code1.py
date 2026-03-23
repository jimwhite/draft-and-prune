from z3 import *

# Singer indices: Kammer=0, Lugo=1, Trillo=2, Waite=3, Yoshida=4, Zinn=5
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-6
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)

# All distinct positions
solver.add(Distinct(pos))

# Recorded auditions: Kammer (0) and Lugo (1)
# Fourth audition cannot be recorded → position 4 must be assigned to non-recorded singer (Trillo, Waite, Yoshida, Zinn)
# Fifth audition must be recorded → position 5 must be assigned to Kammer or Lugo

# Waite constraint: Waite (3) before both recorded auditions
solver.add(pos[3] < pos[0])
solver.add(pos[3] < pos[1])

# Kammer before Trillo
solver.add(pos[0] < pos[2])

# Zinn before Yoshida
solver.add(pos[5] < pos[4])

# Answer choices (as lists of singer names in order)
answer_choices = [
    ["Kammer", "Trillo", "Zinn", "Waite", "Lugo", "Yoshida"],
    ["Waite", "Kammer", "Yoshida", "Zinn", "Lugo", "Trillo"],
    ["Waite", "Lugo", "Kammer", "Trillo", "Zinn", "Yoshida"],
    ["Waite", "Zinn", "Kammer", "Trillo", "Lugo", "Yoshida"],
    ["Zinn", "Yoshida", "Waite", "Lugo", "Kammer", "Trillo"]
]

# Check each answer choice
for idx, order in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert positions based on the order (1-indexed)
    for i, singer in enumerate(order):
        s_chk.add(pos[singers.index(singer)] == i + 1)
    
    # Check if this ordering is possible
    if s_chk.check() == sat:
        print(idx)
        break